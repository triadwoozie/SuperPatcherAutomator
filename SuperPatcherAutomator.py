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

# Step 2: Compress the vbmeta.img using lz4.exe
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

# Step 5: Delete unnecessary files from temp-folder
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
try:
    subprocess.run(command, check=True)
    print(f"Extracted: {super_img}")
except subprocess.CalledProcessError as e:
    print(f"Error during extraction: {e}")

# Step 8: Run SuperPatcherGSI.py to patch the super.img
superpatcher_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SuperPatcherGSI.py')
command = ['python', superpatcher_script, '-i', super_img, '-o', 'output.img', '-s', '2']
try:
    subprocess.run(command, check=True)
    print("SuperPatcherGSI.py executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error running SuperPatcherGSI.py: {e}")

# Step 9: Rename output.img to super.img
output_img = os.path.join(temp_folder, 'output.img')
if os.path.exists(output_img):
    super_img = os.path.join(temp_folder, 'super.img')
    try:
        shutil.move(output_img, super_img)
        print(f"Renamed output.img to super.img at {super_img}")
    except Exception as e:
        print(f"Error renaming output.img to super.img: {e}")
else:
    print(f"Error: output.img not found at {output_img}")

# Step 10: Delete old super.img.lz4 in temp-folder
if os.path.exists(super_img_lz4):
    os.remove(super_img_lz4)
    print(f"Deleted old super.img.lz4 from {temp_folder}")

# Step 11: Compress new super.img into super.img.lz4
new_super_img_lz4 = os.path.join(temp_folder, 'super.img.lz4')
command = [lz4_exe, '-B6', '--content-size', super_img, new_super_img_lz4]
try:
    subprocess.run(command, check=True)
    print(f"Compressed new super.img to {new_super_img_lz4}")
except subprocess.CalledProcessError as e:
    print(f"Error during compression: {e}")

# Step 12: Move the new super.img.lz4 to temp-folder
shutil.move(new_super_img_lz4, super_img_lz4)
print(f"Moved the new super.img.lz4 to {temp_folder}")

# Step 13: Prompt user about rooting
root_choice = input("Do you want to root the device? (yes/no): ").lower()
if root_choice == 'yes':
    patched_file_confirm = input("Have you patched the file according to the XDA guide? (yes/no): ").lower()
    if patched_file_confirm != 'yes':
        print("You need to patch the file as per the XDA guide. Exiting.")
        exit()
    else:
        print("Proceeding with root.")
else:
    print("Proceeding without rooting.")

# Step 14: Move all files from temp-folder to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
for file_name in os.listdir(temp_folder):
    file_path = os.path.join(temp_folder, file_name)
    shutil.move(file_path, os.path.join(script_dir, file_name))
print(f"Moved all files from {temp_folder} to {script_dir}")

# Step 15: Run batch.bat
batch_file = os.path.join(script_dir, 'batch.bat')
try:
    subprocess.run([batch_file], check=True)
    print("batch.bat executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error running batch.bat: {e}")

# Step 16: Inform user about flashing
print("Check the temp-folder for the generated files and use Odin3 to flash your device.")
