import random
import yaml
from gameplay.humanoid import Humanoid
import os


class DataParser(object):
    """
    Parses the input data photos and assigns their file locations to a dictionary for later access
    """
    def __init__(self, data_fp, num_data=100):
        self.unvisited = []
        self.visited = []
        self._build_yaml(data_fp, num_data)
        i = 0
        metadata_fp = os.path.join(data_fp, "metadata.yaml")
        with open(metadata_fp, 'r') as file:
            md = yaml.safe_load(file)
            for h in md['humanoids']:
                if i >= num_data:
                    break
                filename = h["name"]
                pic_fp = os.path.join(data_fp, filename)
                if os.path.isfile(pic_fp) and pic_fp.endswith('.png'):
                    self.unvisited.append(Humanoid(h["name"], h["state"], h["value"], h['time'], h['job']))
                    i += 1
            self.shift_length = md['shift_length']
            self.capacity = md['capacity']

        # sorts and orders the unvisited images based on their time
        random.shuffle(self.unvisited)
        self.unvisited.sort(key=lambda h: h.is_night())

    @staticmethod
    def _build_yaml(data_fp, max_num_data=100):
        shift_length = 1440
        capacity = 9
        classes_values = {'corpse': [0], 'healthy': [1, 2, 5, 10], 'injured': [1, 2, 5, 10], 'zombie': [0]}
        humanoid_list = []
        # assumes each class has a directory within a dataset (and no other dirs exist)
        for path_ in os.listdir(data_fp):
            if os.path.isdir(os.path.join(data_fp, path_)):
                class_str = path_
                class_val_options = classes_values.get(class_str, [0])
                class_val = random.choice(class_val_options)
                for img_file_path in os.listdir(os.path.join(data_fp, path_)):
                    # gets time from the file title
                    # this is like super scuffed we could probably put them into folders instead to make it easier
                    atr = str(img_file_path).split("_")
                    time = atr[2][0]
                    if time not in ['d', 'n']:
                        time = atr[3][0]
                    job = atr[0]
                    pic_dict = {'name': os.path.join(path_, img_file_path),
                                'state': class_str, 'value': class_val, 'time': time, 'job': job}
                    humanoid_list.append(pic_dict)

        # filter humanoid list to the maximum number of images
        # if the available humanoids is more than the max available, sample without replacement
        # otherwise, sample with replacement so that you still get the desired num of images
        if len(humanoid_list) > max_num_data:
            humanoid_list_filtered = random.sample(humanoid_list, k=max_num_data)  # without replacement
        else:
            humanoid_list_filtered = random.choices(humanoid_list, k=max_num_data)  # with replacement
        assert(len(humanoid_list_filtered) == max_num_data)

        # make full dictionary and export into the yaml file
        md_dict = {'shift_length': shift_length, 'capacity': capacity, 'humanoids': humanoid_list_filtered}
        with open(os.path.join(data_fp, "metadata.yaml"), 'w') as f_:
            yaml.dump(md_dict, f_)

    def get_random(self, scorekeeper):
        day_index = 0
        night_index = self.get_first(self.unvisited)
        if len(self.unvisited) == 0:
            raise ValueError("No humanoids remain")
        if scorekeeper.remaining_time >= 12*60:
            humanoid = self.unvisited.pop(day_index)
            self.visited.append(humanoid)
            day_index += 1
        else:
            humanoid = self.unvisited.pop(night_index)
            self.visited.append(humanoid)
            night_index += 1
        return humanoid

    def get_first(self, list):
        for i in range(len(list)):
            if list[i].is_night():
                return i
        else:
            return -1

