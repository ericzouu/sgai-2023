from gameplay.enums import ActionCost
from playsound import playsound
import os
from time import sleep
import logging
import time
import csv
import pandas as pd
from ui_elements.survey_menu import SurveyMenu
from gameplay.humanoid import Humanoid
import os
from b2sdk.v2 import B2Api, InMemoryAccountInfo
import json

class ScoreKeeper(object):
    def __init__(self, shift_len, capacity):
        self.__ambulance = {
            "zombie": 0,
            "injured": 0,
            "healthy": 0,
            "corpse": 0,
        }
        self.__scorekeeper = {
            "killed": 0,
            "saved": 0,
            "suggested": 0,
            "suggestions taken": 0,
        }
        #start of api for data collection
        self.info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.info)
        #Authorization
        self.json= os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gameplay", 'config.json')
        with open(self.json, "r") as jsonfile:
            data = json.load(jsonfile)
        #json keys
        application_key_id = data['application_key_id']
        application_key = data['application_key']

        #gives permission ONLY to edit the files in the bucket, surveydata, and data
        self.b2_api.authorize_account("production", application_key_id, application_key)
        self.bucket_name = 'teamprime'
        #paths for local files
        self.csv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", 'data.csv')
        self.__surveycsv= os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", 'survey.csv')
        self.localcsv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", 'local_data.csv')
        self.localsurveycsv= os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", 'local_survey.csv')
        def copy_data(bucket_name, file_name, local_file_path):
            bucket = self.b2_api.get_bucket_by_name(bucket_name)
            # create a variable for the download
            downloaded_file = bucket.download_file_by_name(file_name)
            # download the file data to a local path
            downloaded_file.save_to(local_file_path)
        copy_data(self.bucket_name, 'survey.csv', self.__surveycsv)
        copy_data(self.bucket_name, 'data.csv', self.csv)
        logging.basicConfig(filename="history.log", encoding='utf-8', level=logging.DEBUG, filemode="w")
        logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1)
        logging.getLogger("playsound").setLevel(logging.CRITICAL + 1)
        self.action_count = 0
        self.__capacity = capacity
        self.remaining_time = int(shift_len)  # minutes
        self.is_disabled = False
        self.last_time = time.time() # time for comparison
        self.is_auto=False
        self.suggested_action = ""
        self.null_human = Humanoid(fp="", state="", value=0)
        self.img_name = ""
        self.__data = pd.DataFrame(columns=['Turn', 'Model', 'Suggested Action', 'Action', 'Target', 'Time Taken',
                                            'Killed', "Saved", "AI Face", 'Job'])
        self.__surveydata= pd.DataFrame(columns=['Result'])
        self.model = "test_net.pth"

    def save(self, humanoid):
        if self.suggested_action == "save":
            self.__scorekeeper["suggestions taken"] += 1
        self.remaining_time -= ActionCost.SAVE.value
        if not self.is_auto:
            playsound(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound', 'saved.mp3'), 0)
        if humanoid.is_zombie():
            self.__ambulance["zombie"] += 1
        elif humanoid.is_injured():
            self.__ambulance["injured"] += 1
        elif humanoid.is_corpse():
            self.__ambulance["corpse"] += 1
        else:
            self.__ambulance["healthy"] += 1
        self.log(humanoid, "SAVE")


    def squish(self, humanoid):
        if self.suggested_action == "squish":
            self.__scorekeeper["suggestions taken"] += 1
        self.remaining_time -= ActionCost.SQUISH.value
        if not self.is_auto:
            playsound(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound', 'squished.mp3'), 0)
        if humanoid.is_healthy() or humanoid.is_injured():
            self.__scorekeeper["killed"] += 1
        self.log(humanoid, "SQUISH")


    def skip(self, humanoid):
        if self.suggested_action == "skip":
            self.__scorekeeper["suggestions taken"] += 1
        self.remaining_time -= ActionCost.SKIP.value
        if not self.is_auto:
            playsound(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound', 'skipped.mp3'), 0)
        if humanoid.is_injured():
            self.__scorekeeper["killed"] += 1
        self.log(humanoid, "SKIP")

    def scram(self, ui=None):
        if self.suggested_action == "scram":
            self.__scorekeeper["suggestions taken"] += 1
            logging.info("suggestion taken")
        self.remaining_time -= ActionCost.SCRAM.value
        if not self.is_auto:
            playsound(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound', 'scrammed.mp3'), 0)
        if self.__ambulance["zombie"] > 0 and self.__ambulance["zombie"] != sum(self.__ambulance.values()):
            self.__scorekeeper["killed"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
            if ui:
                ui.zombie_notif(self.__ambulance["healthy"] + self.__ambulance["injured"])
        else:
            self.__scorekeeper["saved"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
        self.log(self.null_human, "SCRAM")

        if self.remaining_time < ActionCost.SCRAM.value:
            self.remaining_time = 0

        self.__ambulance["zombie"] = 0
        self.__ambulance["injured"] = 0
        self.__ambulance["healthy"] = 0
        self.__ambulance["corpse"] = 0

    def get_current_capacity(self):
        return sum(self.__ambulance.values())

    def at_capacity(self):
        return sum(self.__ambulance.values()) >= self.__capacity

    # counts how often the suggest button is used
    def suggested(self, action):
        self.__scorekeeper["suggested"] += 1
        self.suggested_action = action.lower()

    def get_score(self):
        self.scram()
        print(self.__data)
        self.__data.to_csv(self.csv, mode='a', index=False, header=False)
        self.__data.to_csv(self.localcsv, mode='a', index=False, header=False)
        return self.__scorekeeper
    
    def clock_tick(self, ui):
        while self.remaining_time > 0:
            self.remaining_time -= 1 # decrement by 1 minute
            ui.update_ui(self) # update the ui
            sleep(1)
    
    def record_accuracy(self,variable):
        self.is_disabled = True
        self.__surveydata = pd.DataFrame([variable])
        self.__surveydata.to_csv(self.__surveycsv, mode='a', index=False, header=False)
        self.__surveydata.to_csv(self.localsurveycsv, mode='a', index=False, header=False)
        #Saves Data (calls the function) after ALL the data is saved
        self.savefiles('survey.csv', self.__surveycsv)
        self.savefiles('data.csv', self.csv)
    # Creates an INFO log entry whenever an action is taken
    def log(self, humanoid, action):
        t = time.time() - self.last_time
        self.last_time = time.time()
        row = {'Turn': self.action_count, 'Model': self.model, 'Suggested Action': self.suggested_action,
               'Action': action, 'Target': humanoid.state, 'Time Taken': t, 'Killed': self.__scorekeeper["killed"],
               "Saved": self.__scorekeeper["saved"], "AI Face": self.img_name, 'Job': humanoid.job,
               'File Path': humanoid.fp}
        self.__data = pd.concat([self.__data, pd.DataFrame([row])], ignore_index=True)
        
        self.suggested_action = ""
        self.action_count += 1
    def savefiles(self, file_name, local_file_path):
        #finds the bucket and file to be copied
        bucket = self.b2_api.get_bucket_by_name(self.bucket_name)
        file_info = bucket.get_file_info_by_name(file_name)
        #deletes the file
        bucket.delete_file_version(file_info.id_, file_name)
        # Upload the local file to Backblaze B2 bucket
        bucket.upload_local_file(local_file_path, file_name)