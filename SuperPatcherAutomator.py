import os
import requests
import subprocess
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def download_file(url, dest):
    response = requests.get(url)
    with open(dest, 'wb') as file:
        file.write(response.content)
    logging.info(f"Downloaded {dest}")

def compress_file(input_file, output_file, lz4_exe):
    command = [lz4_exe, '-B6', '--content-size', input_file, output_file]
    subprocess.run(command, check=True)
    logging.info(f"Compressed: {output_file}")

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info(f"Deleted: {file_path}")
    else:
        logging.warning(f"File not found for deletion: {file_path}")

def keep_files(temp_folder, files_to_keep):
    all_files = os.listdir(temp_folder)
    for file_name in all_files:
        if file_name not in files_to_keep:
            remove_file(os.path.join(temp_folder, file_name))

def replace_file(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    shutil.move(src, dst)
    logging.info(f"Replaced: {dst}")

def extract_file(lz4_exe, lz4_file, output_file):
    command = [lz4_exe, '-d', lz4_file, output_file]
    subprocess.run(command, check=True)
    logging.info(f"Extracted: {output_file}")

def move_file_to_script_dir(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join('temp-folder', file_name)
    destination_path = os.path.join(current_dir, file_name)

    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)
        logging.info(f"Moved {file_name} to {current_dir}")
    else:
        logging.warning(f"{file_name} not found in temp-folder for moving.")

def run_super_patcher(super_img):
    output_img = 'super.new.img'
    command = ['python', 'SuperPatcherGSI.py', '-i', super_img, '-o', output_img, '-s', '2']
    
    try:
        subprocess.run(command, check=True)
        logging.info(f"Ran SuperPatcherGSI.py with input: {super_img}, output: {output_img}")
        # Step to rename super.new.img to super.img
        rename_and_compress_output(output_img)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running SuperPatcherGSI.py: {e}")

def rename_and_compress_output(output_img):
    super_img = 'super.img'
    lz4_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lz4.exe')
    temp_folder = 'temp-folder'
    super_img_lz4 = os.path.join(temp_folder, 'super.img.lz4')
    
    # Rename super.new.img to super.img
    if os.path.exists(super_img):
        remove_file(super_img)  # Remove existing super.img if it exists
    shutil.move(output_img, super_img)
    logging.info(f"Renamed {output_img} to {super_img}")
    
    # Compress super.img to super.img.lz4
    compress_file(super_img, super_img_lz4, lz4_exe)
    
    # Move the compressed file into the temp-folder
    replace_file(super_img_lz4, os.path.join(temp_folder, 'super.img.lz4'))

def move_files_out_of_temp_folder(temp_folder):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for file_name in os.listdir(temp_folder):
        source_path = os.path.join(temp_folder, file_name)
        destination_path = os.path.join(current_dir, file_name)
        shutil.move(source_path, destination_path)
        logging.info(f"Moved {file_name} to {current_dir}")
    
    # Delete the temp-folder after moving the files
    shutil.rmtree(temp_folder)
    logging.info(f"Deleted temporary folder: {temp_folder}")

def run_batch_file():
    batch_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'batch.bat')
    try:
        subprocess.run(batch_file, check=True)
        logging.info(f"Executed batch file: {batch_file}")
        
        # Inform the user to check the temp-folder for the generated files
        print("\nPlease check the temp-folder for the generated files.")
        print("Use the generated file to flash your phone using Odin3.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running batch file: {e}")

def check_root():
    response = input("Do you want to root the device? (yes/no): ").strip().lower()
    if response == "yes":
        patched_file_response = input("Have you patched the file according to the XDA guide? (yes/no): ").strip().lower()
        if patched_file_response != "yes":
            logging.warning("Rooting is skipped because the file was not patched according to the guide.")
            return False
    return True

def main():
    if not check_root():
        logging.info("Skipping rooting process.")
        
    url = "https://dl.google.com/developers/android/qt/images/gsi/vbmeta.img"
    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)
    vbmeta_img = os.path.join(temp_dir, 'vbmeta.img')
    download_file(url, vbmeta_img)
    lz4_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lz4.exe')
    vbmeta_img_lz4 = os.path.join(temp_dir, 'vbmeta.img.lz4')
    compress_file(vbmeta_img, vbmeta_img_lz4, lz4_exe)
    remove_file(vbmeta_img)
    temp_folder = 'temp-folder'
    os.makedirs(temp_folder, exist_ok=True)
    input(f"Please place the extracted AP file for your Samsung model in the folder '{temp_folder}', then press Enter to continue...")
    
    files_to_keep = [
        'boot.img.lz4', 'dtbo.img.lz4', 'recovery.img.lz4', 'scp-verified.img.lz4',
        'spmfw-verified.img.lz4', 'sspm-verified.img.lz4', 'super.img.lz4',
        'tee-verified.img.lz4', 'tzar.img.lz4', 'userdata.img.lz4',
        'vbmeta.img.lz4', 'vbmeta_system.img.lz4'
    ]
    keep_files(temp_folder, files_to_keep)
    vbmeta_temp = os.path.join(temp_folder, 'vbmeta.img.lz4')
    replace_file(vbmeta_img_lz4, vbmeta_temp)
    super_img_lz4 = os.path.join(temp_folder, 'super.img.lz4')
    super_img = os.path.join(temp_folder, 'super.img')
    extract_file(lz4_exe, super_img_lz4, super_img)
    
    # Step to move system.img to the script's directory
    move_file_to_script_dir('system.img')
    
    # Step to run SuperPatcherGSI.py with the super.img
    run_super_patcher(super_img)
    
    # Step to move all files from temp-folder to the script's directory
    move_files_out_of_temp_folder(temp_folder)
    
    # Step to run batch.bat
    run_batch_file()

if __name__ == "__main__":
    main()
