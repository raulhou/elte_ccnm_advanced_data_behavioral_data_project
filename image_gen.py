import os
import glob
import random
from PIL import Image, ImageDraw, ImageFont

# Deterministic execution pathing
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()

TARGET_DIRECTORY = os.path.join(SCRIPT_DIR, "stimuli")

def get_next_available_filename(target_folder, prefix, flip_suffix, extension=".png"):
    """
    Constructs the filename with the specific flip suffix.
    Note: We do not use 'highest index' tracking here because the suffix 
    changes per file, which would break simple sequential detection. 
    Instead, we use a counter provided by the loop.
    """
    os.makedirs(target_folder, exist_ok=True)
    return os.path.join(target_folder, f"{prefix}{flip_suffix}{extension}")

def generate_psychological_stimulus(number_group, file_path):
    """Renders visual stimuli and saves to the specifically constructed path."""
    scale_factor = 4 
    canvas_width = 1600
    canvas_height = 800
    background_color = (169, 169, 169) 
    
    image = Image.new("RGB", (canvas_width, canvas_height), background_color)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()

    dimensions = [
        (number_group[0] * scale_factor, number_group[1] * scale_factor),
        (number_group[2] * scale_factor, number_group[3] * scale_factor),
        (number_group[4] * scale_factor, number_group[5] * scale_factor)
    ]
    
    spacing_interval = canvas_width // 4
    base_y_alignment = 600 
    
    for index, (height, width) in enumerate(dimensions):
        center_x = spacing_interval * (index + 1)
        left_bound = center_x - (width // 2)
        right_bound = center_x + (width // 2)
        top_bound = base_y_alignment - height
        bottom_bound = base_y_alignment
        
        draw.rectangle([left_bound, top_bound, right_bound, bottom_bound], fill=(0, 0, 0))
        label_text = str(index + 1)
        draw.text((center_x - 20, base_y_alignment + 30), label_text, fill=(0, 0, 0), font=font)
        
    image.save(file_path)

def process_batch(dataset_string, file_prefix, group_name):
    """
    Parses a dataset and executes the rendering loop. 
    Resets the random seed at the start of every batch to ensure 
    identical flip sequences across groups.
    """
    # RESET SEED for synchronization across groups
    random.seed(42)
    
    parsed_data_arrays = [
        [int(value) for value in line.split()] 
        for line in dataset_string.strip().split('\n') if line.strip()
    ]

    print(f"\n--- Processing {group_name} ---")
    
    for i, data_row in enumerate(parsed_data_arrays):
        active_row = list(data_row)
        file_index = f"{i+1:02d}" # Create 01, 02, etc.
        
        # 50% probability swap
        if random.random() < 0.5:
            # Flip Logic (Swap Figure 1 and 3)
            active_row[0], active_row[4] = active_row[4], active_row[0] 
            active_row[1], active_row[5] = active_row[5], active_row[1] 
            flip_label = "flip1"
        else:
            flip_label = "flip0"
        
        # Construct filename: e.g., wt_d1_01_flip1.png
        full_prefix = f"{file_prefix}{file_index}_{flip_label}"
        save_path = os.path.join(TARGET_DIRECTORY, f"{full_prefix}.png")
        
        generate_psychological_stimulus(active_row, save_path)
        print(f"Saved: {full_prefix}.png")

# --- DATASETS ---

wt_d1_data = """77 41 77 33 41 77
77 41 77 32 41 77
77 46 77 38 46 77
77 46 77 37 46 77
77 51 77 43 51 77
77 51 77 42 51 77
82 41 82 33 41 82
82 41 82 32 41 82
82 46 82 38 46 82
82 46 82 37 46 82
82 51 82 43 51 82
82 51 82 42 51 82
87 41 87 33 41 87
87 41 87 32 41 87
87 46 87 38 46 87
87 46 87 37 46 87
87 51 87 43 51 87
87 51 87 42 51 87"""

ht_d1_data = """41 77 33 77 77 41
41 77 32 77 77 41
41 82 33 82 82 41
41 82 32 82 82 41
41 87 33 87 87 41
41 87 32 87 87 41
46 77 38 77 77 46
46 77 37 77 77 46
46 82 38 82 82 46
46 82 37 82 82 46
46 87 38 87 87 46
46 87 37 87 87 46
51 77 43 77 77 51
51 77 42 77 77 51
51 82 43 82 82 51
51 82 42 82 82 51
51 87 43 87 87 51
51 87 42 87 87 51"""

wt_d0_data = """77 41 36 33 41 77
77 41 36 32 41 77
77 46 41 38 46 77
77 46 41 37 46 77
77 51 46 43 51 77
77 51 46 42 51 77
82 41 36 33 41 82
82 41 36 32 41 82
82 46 41 38 46 82
82 46 41 37 46 82
82 51 46 43 51 82
82 51 46 42 51 82
87 41 36 33 41 87
87 41 36 32 41 87
87 46 41 38 46 87
87 46 41 37 46 87
87 51 46 43 51 87
87 51 46 42 51 87"""

ht_d0_data = """41 77 33 36 77 41
41 77 32 36 77 41
41 82 33 36 82 41
41 82 32 36 82 41
41 87 33 36 87 41
41 87 32 36 87 41
46 77 38 41 77 46
46 77 37 41 77 46
46 82 38 41 82 46
46 82 37 41 82 46
46 87 38 41 87 46
46 87 37 41 87 46
51 77 43 46 77 51
51 77 42 46 77 51
51 82 43 46 82 51
51 82 42 46 82 51
51 87 43 46 87 51
51 87 42 46 87 51"""

# --- EXECUTION ---

print(f"Target Directory: {TARGET_DIRECTORY}")

process_batch(wt_d1_data, "wt_d1_", "Width Target Decoy")
process_batch(ht_d1_data, "ht_d1_", "Height Target Decoy")
process_batch(wt_d0_data, "wt_d0_", "Width Target None Decoy")
process_batch(ht_d0_data, "ht_d0_", "Height Target None Decoy")

print("\n=== Generation Complete. Sequences are synchronized. ===")
