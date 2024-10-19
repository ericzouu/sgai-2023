# SGAI_2023

## Dependencies:
- PIL
  - `pip3 install pillow`
- TKinter
  - `pip3 install tk`
- Pytorch 
  - `pip3 install torch`
- Playsound
  - `pip install playsound2`
    !Do not use the playsound module, if it is installed, please uninstall it and download playsound2!
- Pyglet
  - `pip install pyglet`
- Pandas
  - `pip install pandas`
- Backblaze SDK
  - `pip install b2sdk`

To run, type "python3 main.py" in the terminal.

## Gameplay

You are controlling an ambulance with the goal of saving as many humans as possible in a zombie apocalypse. Accidentally killing humans will detract from your score, while saving them will increase it. To optimize your score, you have five available actions and 24 hours.

**SKIP**: Skips the humanoid. If the humanoid is injured, this will mark them as killed. This action takes 15 minutes and can also be accessed by pressing "Q".

**SQUISH**: Squishes the humanoid. If the humanoid is injured or healthy, this will mark them as killed. This action takes 5 minutes and can also be accessed by pressing "W".

**SAVE**: Saves the humanoid. If the humanoid is injured or healthy, this will mark them as saved IF they are returned safely to the hospital. If a zombie is saved, they will kill all of the humans in the ambulance, resulting in all of them being marked as killed. This action takes 30 minutes and can also be accessed by pressing "E".

**SCRAM**: Returns to the hospital. This action takes 2 hours and can be accessed by pressing "R".

**SUGGEST**: Sometimes, *obstructions* will appear, causing the viewer to be blocked. These obstructions can make it difficult to detect the type of the humanoid, however, the SUGGEST button can be prompted. This button allows the AI to suggest an action, without its view being blocked by the obstructions. This action takes no time and can also be accessed by pressing SPACE.

There are multiple AI models being used in the experiment--some accurate and some inaccurate. You will be informed of the model used at the start screen, so keep it in mind.
Once you complete the game do not share your results until data collection is over
