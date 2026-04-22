from psychopy import visual, core, event, gui
import os
import glob
import random
import csv

# --- Initialization ---
exp_name = 'Size_Judgment_Task'
exp_info = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
if not dlg.OK: core.quit()

script_dir = os.path.dirname(os.path.abspath(__file__))
stim_path = os.path.join(script_dir, 'stimuli')
data_path = os.path.join(script_dir, 'data')
if not os.path.exists(data_path): os.makedirs(data_path)

log_file_path = os.path.join(data_path, f"{exp_info['participant']}_results.csv")

image_files = glob.glob(os.path.join(stim_path, "*.png"))
# Remove fixation from the trial list to prevent it from being tested
image_files = [f for f in image_files if "fixation.png" not in f]

if not image_files:
    print(f"Error: No stimulus files found in {stim_path}")
    core.quit()

random.shuffle(image_files)

# Setup Window
win = visual.Window(size=[1600, 900], fullscr=True, monitor="testMonitor", units="pix", color=[0.66, 0.66, 0.66])
stim_image = visual.ImageStim(win=win)

# Fixation Setup
fixation_path = os.path.join(stim_path, 'fixation.png')
if not os.path.exists(fixation_path):
    fixation_stim = visual.TextStim(win=win, text="+", color=(-1, -1, -1), height=50)
else:
    fixation_stim = visual.ImageStim(win=win, image=fixation_path)

# --- Instruction Screen ---
instruction_text = (
    "WELCOME TO THE EXPERIMENT\n\n"
    "In each trial, you will see three black figures labeled 1, 2, and 3.\n"
    "Your task is to identify which figure is the BIGGEST.\n\n"
    "Respond by pressing the corresponding number on your keyboard:\n"
    "Press '1' for the Left figure\n"
    "Press '2' for the Middle figure\n"
    "Press '3' for the Right figure\n\n"
    "The next trial will begin immediately after you make a choice.\n"
    "You have a maximum of 5 seconds to respond per image.\n\n"
    "PRESS ANY KEY TO BEGIN"
)

instr_stim = visual.TextStim(win=win, text=instruction_text, color=(-1, -1, -1), 
                             height=30, wrapWidth=1000, alignText='center')

instr_stim.draw()
win.flip()

# Wait for any key press to start
event.waitKeys()

# Create CSV and write header
with open(log_file_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Participant', 'Image_File', 'Response_Key', 'Reaction_Time_Seconds'])

# --- Experiment Loop ---
for img_path in image_files:
    # 1. Fixation Image (1.0s duration)
    fixation_stim.draw()
    win.flip()
    core.wait(1.0)
    
    # 2. Stimulus Presentation (Max 5.0s duration)
    stim_image.setImage(img_path)
    stim_image.draw()
    win.flip()
    
    rt_clock = core.Clock()
    event.clearEvents()
    
    trial_response = "None"
    trial_rt = "NaN"
    
    while rt_clock.getTime() < 5.0:
        keys = event.getKeys(keyList=['1', '2', '3', 'escape'], timeStamped=rt_clock)
        if keys:
            key, time = keys[0]
            if key == 'escape':
                win.close()
                core.quit()
            
            # Record response and immediately break the loop
            trial_response = key
            trial_rt = time
            break
        
    # 3. Data Logging
    file_name = os.path.basename(img_path)
    with open(log_file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([exp_info['participant'], file_name, trial_response, trial_rt])

# --- Final Screen ---
end_stim = visual.TextStim(win=win, text="Thank you for participating.\n\nExperiment Complete.", color=(-1, -1, -1))
end_stim.draw()
win.flip()
core.wait(2.0)

win.close()
core.quit()