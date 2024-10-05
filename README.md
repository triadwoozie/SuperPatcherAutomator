# SuperPatcherAutomator

**SuperPatcherAutomator** is an automated Python script designed to simplify the process of preparing Generic System Images (GSIs) for flashing on Samsung devices using Odin3. This comprehensive tool streamlines the entire workflow, from downloading necessary files to compressing and preparing the final output, ensuring an efficient and user-friendly experience for both novice and experienced users.

## Features

- **Automated Downloading:** Downloads the required `vbmeta.img` file from a reliable source, eliminating manual download efforts.
- **LZ4 Compression:** Compresses images to save space and enhance performance during the flashing process.
- **User Prompts:** Guides users through the process with clear prompts for placing files and instructions for the next steps.
- **File Management:** Cleans up unnecessary files and moves essential images to the appropriate locations, preventing clutter and confusion.
- **Integration with SuperPatcherGSI:** Seamlessly runs the SuperPatcherGSI script to modify the `super.img`, preparing it for use with Odin3.
- **Post-Execution Instructions:** Informs users on the next steps, including how to flash their devices with Odin3.

## Requirements

- **Python 3.x:** Ensure you have Python installed on your machine.
- **LZ4 Executable:** Download and place `lz4.exe` in the same directory as the script.
- **SuperPatcherGSI.py:** Include this script in the same directory to handle image patching.
- **Internet Access:** Required for downloading the necessary files.

## Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/SuperPatcherAutomator.git
   cd SuperPatcherAutomator
   ```

2. **Prepare Required Files:**
   - Ensure `lz4.exe` and `SuperPatcherGSI.py` are present in the same directory as the script.

3. **Run the Script:**
   ```bash
   python SuperPatcherAutomator.py
   ```

4. **Follow Prompts:**
   - The script will prompt you to place the extracted AP file for your Samsung model in a designated folder. Follow the instructions carefully.

5. **Completion:**
   - Once the script finishes, check the output in the specified directory. You will receive instructions on how to use the generated files with Odin3 to flash your device.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for enhancements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
