import os
import glob
import random
from PIL import Image, ImageDraw, ImageFont

# Deterministic execution enforced for reproducibility across both groups
random.seed(42)

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()

TARGET_DIRECTORY = os.path.join(SCRIPT_DIR, "stimuli")

def get_next_available_filename(target_folder, prefix, extension=".png"):
    """Tracks existing files with the dynamically selected prefix."""
    os.makedirs(target_folder, exist_ok=True)
    search_pattern = os.path.join(target_folder, f"{prefix}*{extension}")
    existing_files = glob.glob(search_pattern)
    
    highest_index = 0
    for file_path in existing_files:
        filename = os.path.basename(file_path)
        index_str = filename.replace(prefix, "").replace(extension, "")
        if index_str.isdigit():
            highest_index = max(highest_index, int(index_str))
            
    next_index = highest_index + 1
    next_filename = f"{prefix}{next_index:02d}{extension}"
    return os.path.join(target_folder, next_filename)

def generate_psychological_stimulus(number_group, file_prefix):
    """Renders visual stimuli and saves using the designated prefix."""
    if len(number_group) != 6:
        raise ValueError("Fatal Error: Invalid data row detected. Must contain 6 numbers.")
    
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
        
    output_filepath = get_next_available_filename(TARGET_DIRECTORY, prefix=file_prefix)
    image.save(output_filepath)
    print(f"Success: Saved {output_filepath} using parameters {number_group}.")

# --- DATASETS ---

raw_dataset_dominant = """77 41 77 33 41 77
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
87 51 87 42 51 87
41 77 33 77 77 41
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

raw_dataset_none_dominant = """77 41 36 33 41 77
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
87 51 46 42 51 87
41 77 33 36 77 41
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

def process_batch(dataset_string, file_prefix, group_name):
    """Parses a dataset and executes the rendering loop with randomization."""
    parsed_data_arrays = []
    for line in dataset_string.strip().split('\n'):
        if line.strip():
            parsed_data_arrays.append([int(value) for value in line.split()])

    print(f"\n--- Generating {len(parsed_data_arrays)} images for the {group_name} ---")
    
    for data_row in parsed_data_arrays:
        active_row = list(data_row)
        
        # 50% probability swap applied independently per row
        if random.random() < 0.5:
            active_row[0], active_row[4] = active_row[4], active_row[0] 
            active_row[1], active_row[5] = active_row[5], active_row[1] 
        
        generate_psychological_stimulus(active_row, file_prefix)

# --- EXECUTION TRIGGER ---

print("=== AUTOMATED STIMULUS GENERATION PROTOCOL ===")
print(f"Target Directory: {TARGET_DIRECTORY}")

# Execute both batches consecutively
process_batch(raw_dataset_dominant, "d1_", "dominant group")
process_batch(raw_dataset_none_dominant, "d0_", "none dominant group")

print("\n=== All batches completed successfully ===")