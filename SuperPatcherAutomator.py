import os
import requests
import subprocess
import shutil

# Step 1: Download vbmeta.img file
url = "https://dl.google.com/developers/android/qt/images/gsi/vbmeta.img"
temp_dir = 'temp'
os.makedirs(temp_dir, exist_ok=True)
vbmeta_img = os.path.join(temp_dir, 'vbmeta.img')

response = requests.get(url)
with open(vbmeta_img, 'wb') as file:
    file.write(response.content)
print(f"Downloaded vbmeta.img to {vbmeta_img}")

# Step 2: Compress vbmeta.img using lz4.exe
lz4_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lz4.exe')
vbmeta_img_lz4 = os.path.join(temp_dir, 'vbmeta.img.lz4')

command = [lz4_exe, '-B6', '--content-size', vbmeta_img, vbmeta_img_lz4]
try:
    subprocess.run(command, check=True)
    print(f"Compression successful: {vbmeta_img_lz4}")
except subprocess.CalledProcessError as e:
    print(f"Error during compression: {e}")

# Step 3: Delete the original vbmeta.img file
os.remove(vbmeta_img)
print(f"Deleted original file: {vbmeta_img}")

# Step 4: Create temp-folder and prompt user
temp_folder = 'temp-folder'
os.makedirs(temp_folder, exist_ok=True)
input(f"Please place the extracted AP file for your Samsung model in the folder '{temp_folder}', then press Enter to continue...")

# Step 5: Delete all files except the ones listed in the image
files_to_keep = [
    'boot.img.lz4', 'dtbo.img.lz4', 'recovery.img.lz4', 'scp-verified.img.lz4',
    'spmfw-verified.img.lz4', 'sspm-verified.img.lz4', 'super.img.lz4',
    'tee-verified.img.lz4', 'tzar.img.lz4', 'userdata.img.lz4',
    'vbmeta.img.lz4', 'vbmeta_system.img.lz4'
]

all_files = os.listdir(temp_folder)

for file_name in all_files:
    if file_name not in files_to_keep:
        file_path = os.path.join(temp_folder, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_name}")
        except Exception as e:
            print(f"Error deleting {file_name}: {e}")

# Step 6: Replace vbmeta.img.lz4 in temp-folder with the one downloaded
vbmeta_temp = os.path.join(temp_folder, 'vbmeta.img.lz4')
if os.path.exists(vbmeta_temp):
    os.remove(vbmeta_temp)
shutil.move(vbmeta_img_lz4, vbmeta_temp)
print(f"Replaced vbmeta.img.lz4 in {temp_folder}")

# Step 7: Extract super.img.lz4 to create super.img
super_img_lz4 = os.path.join(temp_folder, 'super.img.lz4')
super_img = os.path.join(temp_folder, 'super.img')

# Command to extract the lz4 file
command = [lz4_exe, '-d', super_img_lz4, super_img]

# Execute the command to extract super.img.lz4
try:
    subprocess.run(command, check=True)
    print(f"Extracted: {super_img}")
except subprocess.CalledProcessError as e:
    print(f"Error during extraction: {e}")

# Step 8: Run SuperPatcherGSI.py with specific flags
super_patcher_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SuperPatcherGSI.py')
command = ['python', super_patcher_script, '-i', super_img, '-o', 'output.img', '-s', '2']

try:
    subprocess.run(command, check=True)
    print("SuperPatcherGSI.py script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error running SuperPatcherGSI.py: {e}")

# Step 9: Rename output.img to super.img, replacing the old super.img
output_img = os.path.join(temp_folder, 'output.img')
if os.path.exists(super_img):
    os.remove(super_img)
os.rename(output_img, super_img)
print(f"Renamed output.img to {super_img}")

# Step 10: Delete the old super.img.lz4 in temp-folder
if os.path.exists(super_img_lz4):
    os.remove(super_img_lz4)
print(f"Deleted old super.img.lz4 in {temp_folder}")

# Step 11: Compress the new super.img into super.img.lz4
super_img_lz4 = os.path.join(temp_folder, 'super.img.lz4')
command = [lz4_exe, '-B6', '--content-size', super_img, super_img_lz4]

try:
    subprocess.run(command, check=True)
    print(f"Compressed {super_img} to {super_img_lz4}")
except subprocess.CalledProcessError as e:
    print(f"Error during compression: {e}")

# Ensure old super.img.lz4 is not used (already deleted in Step 10)

# Step 12: Move super.img.lz4 into temp-folder
shutil.move(super_img_lz4, os.path.join(temp_folder, 'super.img.lz4'))
print(f"Moved new super.img.lz4 into {temp_folder}")

# Step 13: Delete all .img files in the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
for file_name in os.listdir(script_dir):
    if file_name.endswith('.img'):
        os.remove(os.path.join(script_dir, file_name))
print("Deleted all .img files in the script directory")

# Step 14: Ask user if they want to root
root = input("Do you want to root the device? (yes/no): ").strip().lower()

if root == 'yes':
    confirmation = input("Have you patched the file according to the XDA guide? (yes/no): ").strip().lower()
    if confirmation != 'yes':
        print("Please patch the file according to the XDA guide, then run the script again.")
        exit(1)

# Step 15: Run batch.bat
batch_file = os.path.join(script_dir, 'batch.bat')
try:
    subprocess.run(batch_file, check=True)
    print("batch.bat executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error running batch.bat: {e}")

# Step 16: Inform the user to check temp-folder for flashing files
print(f"Process complete. Please check the '{temp_folder}' for the files needed to flash your phone using Odin3.")