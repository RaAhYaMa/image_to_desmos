# Image to Desmos Art Converter

This project processes images, applies Canny edge detection, and converts the edges into SVG and HTML files for visualization in Desmos.

## Features
- Automatically detects image files in the current directory.
- Allows user selection of an image file.
- Applies Canny edge detection with adjustable threshold values.
- Generates BMP, SVG, and HTML files for visualization.
- Uses Desmos API to display the processed edges as mathematical expressions.

## Prerequisites
- Python 3.x
- `pip` package manager
- `virtualenv` (recommended for environment isolation)

## Installation & Setup
Follow the instructions based on your operating system:

### Windows
1. Open Command Prompt or PowerShell.
2. Clone the repository or download the project files.
3. Navigate to the project directory:
   ```sh
   cd path/to/project
   ```
4. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
5. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
6. Install Potrace (required for SVG conversion):
   - Download Potrace for Windows: [https://potrace.sourceforge.net](https://potrace.sourceforge.net)
   - Extract the files and add the extracted directory to the system `PATH`.

### Linux
1. Open a terminal.
2. Clone the repository or download the project files.
3. Navigate to the project directory:
   ```sh
   cd path/to/project
   ```
4. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
5. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
6. Install Potrace:
   ```sh
   sudo apt update && sudo apt install potrace
   ```
   *(For Arch Linux users, install with: `sudo pacman -S potrace`)*

### macOS
1. Open a terminal.
2. Clone the repository or download the project files.
3. Navigate to the project directory:
   ```sh
   cd path/to/project
   ```
4. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
5. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
6. Install Potrace:
   ```sh
   brew install potrace
   ```

## Running the Program
Once everything is set up, you can run the program by executing:
```sh
python main.py
```
Follow the on-screen prompts to select an image, adjust edge detection, and generate the output files.

## Output
After processing, the following files will be generated:
- **BMP file** (Edge-detected version of the input image)
- **SVG file** (Vector representation of the edges)
- **HTML file** (Visual representation using Desmos API)

Open the generated `.html` file in a web browser to view your Desmos-generated art.

## Contributions
Feel free to submit issues and pull requests to improve this project!

## License & Usage
This project is released under an open-source license but **must not be commercialized**. Any form of monetization, including selling, licensing, or using it for commercial purposes, is strictly prohibited.

