# SuperPatcherAutomator

**SuperPatcherAutomator** is a comprehensive tool designed to streamline and automate the process of preparing system images for devices with dynamic super partitions, simplifying custom ROM flashing and optional rooting via Odin3. This tool eliminates many of the manual steps involved in patching system images and handling `super.img` files, particularly on Samsung devices. 

It automates key steps of the [XDA Guide](https://xdaforums.com/t/guide-custom-how-to-install-custom-rom-using-odin-without-twrp-phh-lineageos.4114435/) for devices using super partitions, providing a more seamless experience for users looking to customize their Android devices.

### What is a Super Partition?

Super partitions are dynamic containers introduced in Android devices to allow the resizing of partitions like system, vendor, and product without affecting the overall partition structure. This flexibility is key for modern Android devices. For more information on super partitions, check out the official Android documentation [here](https://source.android.com/docs/core/ota/dynamic_partitions/implement).

## How It Works

**SuperPatcherAutomator** automates each step required to patch, compress, and prepare system image files for flashing on Android devices with super partitions. Below is a detailed walkthrough of what the program does:

### Detailed Step-by-Step Workflow:

1. **Download `vbmeta.img`**:
    - The script starts by downloading `vbmeta.img` from Google’s official server and saves it in a `temp` directory. This file is necessary for flashing Android devices.
  
2. **Compress `vbmeta.img` using LZ4**:
    - Once downloaded, the script compresses `vbmeta.img` into `vbmeta.img.lz4` using `lz4.exe`.
    - The LZ4 compression tool is crucial for handling `.img` files in formats required by Odin3 and other flashing tools.
  
3. **Clean Up Unnecessary Files**:
    - The script will delete the original uncompressed `vbmeta.img` after compression to ensure only necessary files are kept.
  
4. **User Interaction for Placing Files**:
    - The script prompts the user to place their extracted AP file for the device into a `temp-folder` directory. This file contains all the essential components of the system images, such as boot, recovery, and super images.
  
5. **Delete Unnecessary `.img` Files**:
    - It then scans the `temp-folder` and deletes any file that isn't on a list of critical `.img.lz4` files, such as `boot.img.lz4`, `super.img.lz4`, and others necessary for flashing.
  
6. **Replace `vbmeta.img.lz4`**:
    - The previously downloaded and compressed `vbmeta.img.lz4` is copied into the `temp-folder`, replacing any existing version of `vbmeta.img.lz4` to ensure the correct file is used during flashing.

7. **Extract `super.img.lz4`**:
    - The script decompresses `super.img.lz4` into `super.img`, preparing it for further processing and patching.

8. **Run SuperPatcherGSI**:
    - **SuperPatcherGSI.py** is executed with specific flags (`-i super.img -o output.img -s 2`), which patches the `super.img` based on the user's custom ROM and device.
    - This step automates a previously manual process of modifying the super partition for compatibility with custom ROMs and GSI (Generic System Image).

9. **Rename and Replace `super.img`**:
    - The patched `output.img` from **SuperPatcherGSI** is renamed to `super.img`, replacing the previous version. The script ensures that the patched image is used in all subsequent steps.

10. **Delete Old and Compress New `super.img.lz4`**:
    - The script deletes any existing `super.img.lz4` in the temp folder and compresses the newly patched `super.img` into `super.img.lz4`. This is essential for flashing, as Odin3 expects `.lz4` compressed images.

11. **Delete Old `.img` Files**:
    - After the patched `super.img.lz4` is prepared, all the original `.img` files in the script directory are deleted to avoid confusion and ensure only the patched files remain.

12. **Move Files to Script Directory**:
    - The script moves all necessary files from the `temp-folder` back to the directory where the script is located, consolidating the files needed for the next steps.

13. **Rooting Option**:
    - The script prompts the user whether they want to root their device or not. If the user opts for rooting, it asks for confirmation that the `super.img` has been patched according to the XDA guide. If the patching is confirmed, the script proceeds with flashing. Otherwise, it warns the user to follow the guide first.
  
14. **Inform the User About Flashing**:
    - The script informs the user that all necessary files are in the `temp-folder`, and they can use Odin3 to flash their device.

### Python Version Usage

1. Make sure Python 3.x is installed.
2. Place `lz4.exe`, `SuperPatcherGSI.py`, and any other required files in the same directory as the Python script.
3. Run the Python script:
   ```bash
   python SuperPatcherAutomator.py
   ```
4. Follow the prompts to place the extracted AP file into the `temp-folder` and choose whether to root the device.
5. The script will patch, compress, and move all necessary files automatically.

## Sources and Credit

- **SuperPatcherGSI**: Special thanks to [SuperPatcherGSI](https://github.com/ChromiumOS-Guy/SuperPatcherGSI) for the tool used to patch `super.img`.
- **LZ4**: Compression and decompression are performed using [LZ4](https://github.com/lz4/lz4).
- **lpmake for Linux**: Obtained from [AOSP-master builds](https://ci.android.com/builds/branches/aosp-master/grid).
- **lpmake for Windows**: From [lpmake Windows version](https://github.com/affggh/lpmake_and_lpunpack_cygwin).
- **lpunpack.py**: [Lpunpack project](https://github.com/unix3dgforce/lpunpack), compiled to `.exe` for the Windows version.

## Fixes and Issues

Ensure all required Python libraries are installed before running the Python script. The program uses standard libraries, but if you encounter any issues with missing dependencies, install them via pip. 

## Warning

**Backup your data!** This script modifies system partitions and can potentially brick your device if not used correctly. **I am not responsible for any damage to your device.** Follow the instructions carefully and proceed at your own risk.

## Guide Automation

This tool automates many steps of the [XDA Guide](https://xdaforums.com/t/guide-custom-how-to-install-custom-rom-using-odin-without-twrp-phh-lineageos.4114435/) for devices with super partitions, allowing users to flash custom ROMs without the need for TWRP.
