import cv2 as cv
import os
import subprocess
from svgpathtools import svg2paths
import json

def get_image_files():
    """
    Get a list of all image files in the current directory

    Returns
    -------
    dict
        A dictionary where the keys are the numbers of the image files,
        and the values are the names of the image files.
    """
    image_files = {}
    image_count = 0
    for file in os.listdir():
        # Check if the file is an image file
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
            image_count += 1
            image_files[image_count] = file
    return image_files

def select_image(image_files):
    """
    Select an image file from the given list

    Parameters
    ----------
    image_files : dict
        A dictionary where the keys are the numbers of the image files,
        and the values are the names of the image files.

    Returns
    -------
    str
        The name of the selected image file
    """
    print("List of images in this folder:")
    for index, file in image_files.items():
        print(f"{index}: {file}")
    while True:
        index = input(f"Choose one of it (1{' - ' + str(len(image_files)) if len(image_files) > 1 else ''}): ")
        try:
            # Get the selected image file based on the given index
            img_dir = image_files[int(index)]
            if not os.path.exists(img_dir):
                print("Error: Image file does not exist.")
                continue
            if not os.path.isfile(img_dir):
                print("Error: Selected file is not an image file.")
                continue
            # Break the loop if the image file is valid
            break
        except:
            print("Invalid index")
    return img_dir

def apply_canny_edge_detection(img):
    """
    Apply Canny edge detection to a given image

    Parameters
    ----------
    img : numpy.ndarray
        The input image

    Returns
    -------
    numpy.ndarray
        The output image with Canny edge detection applied
    """
    cv.namedWindow('canny')
    cv.createTrackbar("minThres", 'canny', 0, 255, lambda x: None)
    cv.createTrackbar("maxThres", 'canny', 0, 255, lambda x: None)
    print("\nSlide or input the minThres and maxThres values")
    print("Click 'q' if you are done with the settings")
    while True:
        # Wait for a key press
        if cv.waitKey(1) & 0xFF == ord('q'):
            # Break the loop if 'q' is pressed
            break
        # Get the current values of the trackbars
        min_thres = cv.getTrackbarPos('minThres', 'canny')
        max_thres = cv.getTrackbarPos('maxThres', 'canny')
        # Apply Canny edge detection
        canny = cv.Canny(img, min_thres, max_thres)
        # Display the output image
        cv.imshow('canny', canny)
    # Close all OpenCV windows
    cv.destroyAllWindows()
    return canny

def generate_output_files(canny, name):
    """
    Generate output files (BMP, SVG and HTML) from the given image

    Parameters
    ----------
    canny : numpy.ndarray
        The input image with Canny edge detection applied
    name : str
        The name of the output files
    """
    try:
        cv.imwrite(f"{name}.bmp", canny)
    except Exception as e:
        print(f"Error: Failed to write BMP file - {e}")
        return
    try:
        subprocess.run(["potrace", "--svg", f"{name}.bmp", "-o", f"{name}.svg"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to generate SVG file - {e}")
        return
    try:
        paths, _ = svg2paths(f"{name}.svg")
    except Exception as e:
        print(f"Error: Failed to parse SVG file - {e}")
        return

    print(f"\nMaking {name}.html")
    data = []
    count = 0
    for path in paths:
        for segment in path:
            count += 1
            segment_data = {}
            segment_data["type"] = "expression"
            segment_data["id"] = f"{count}"
            segment_data["color"] = "#000000"
            if segment.__class__.__name__ == "Line":
                segment_data["latex"] = f"(({int(segment.start.real)}) + ({int(segment.end.real - segment.start.real)}) t, ({int(segment.start.imag)}) + ({int(segment.end.imag - segment.start.imag)}) t)\n"
            elif segment.__class__.__name__ == "QuadraticBezier":
                segment_data["latex"] = f"({int(segment.start.real)} (1 - t)^2 + ({int(2 * segment.control.real)}) (t - t^2) + ({int(segment.end.real)}) t, {int(segment.start.imag)} (1 - t)^2 + ({int(2 * segment.control.imag)}) (t - t^2) + ({int(segment.end.imag)}) t)\n"
            elif segment.__class__.__name__ == "CubicBezier":
                segment_data["latex"] = f"(({int(segment.start.real)}) (1 - t)^3 + ({int(3 * segment.control1.real)}) (1 - t)^2 t + ({int(3 * segment.control2.real)}) (1 - t) t^2 + ({int(segment.end.real)}) t^3, ({int(segment.start.imag)}) (1 - t)^3 + ({int(3 * segment.control1.imag)}) (1 - t)^2 t + ({int(3 * segment.control2.imag)}) (1 - t) t^2 + ({int(segment.end.imag)}) t^3)\n"
            data.append(segment_data)
    width = int(img.shape[1] * 1.2)
    height = int(img.shape[0] * 1.2)
    html_content = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <script src="https://www.desmos.com/api/v1.10/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"></script>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                height: 100%;
            }}
            #calculator {{
                height: 100%;
                width: 100%;
            }}
            #loading-screen {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(255, 255, 255, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
                font-family: Arial, sans-serif;
                font-size: 1.5em;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div id="loading-screen">
            <p>Loading graph, please wait...</p>
        </div>

        <div id="calculator"></div>
    </body>
    <script>
        var elt = document.getElementById('calculator');
        var calculator = Desmos.GraphingCalculator(elt);

        function showLoadingScreen() {{
            document.getElementById('loading-screen').style.display = 'flex';
        }}

        function hideLoadingScreen() {{
            document.getElementById('loading-screen').style.display = 'none';
        }}

        function setZoomSquare(calculator) {{
            const pixelCoords = calculator.graphpaperBounds.pixelCoordinates;
            const mathCoords = calculator.graphpaperBounds.mathCoordinates;

            const pixelsPerUnitX = pixelCoords.width / mathCoords.width;
            const pixelsPerUnitY = pixelCoords.height / mathCoords.height;

            let newMathBounds;
            if (pixelsPerUnitX > pixelsPerUnitY) {{
                const newWidth = mathCoords.width * (pixelsPerUnitX / pixelsPerUnitY);
                const xCenter = (mathCoords.left + mathCoords.right) / 2;
                newMathBounds = {{
                left: xCenter - newWidth / 2,
                right: xCenter + newWidth / 2,
                bottom: mathCoords.bottom,
                top: mathCoords.top,
                }};
            }} 
            else {{
                const newHeight = mathCoords.height * (pixelsPerUnitY / pixelsPerUnitX);
                const yCenter = (mathCoords.bottom + mathCoords.top) / 2;
                newMathBounds = {{
                left: mathCoords.left,
                right: mathCoords.right,
                bottom: yCenter - newHeight / 2,
                top: yCenter + newHeight / 2,
                }};
            }}

            calculator.setMathBounds(newMathBounds);
        }}
        function initGraph() {{
            showLoadingScreen();
            state = calculator.getState();
            state.expressions.list = {json.dumps(data)};
            calculator.setState(state);
            calculator.setMathBounds({{
                left: -{width},
                right: {width}0,
                bottom: -{height},
                top: {height}0
            }});
            calculator.updateSettings({{showGrid: false}});
            setZoomSquare(calculator);
            calculator.asyncScreenshot({{}}, function () {{
                hideLoadingScreen();
            }});
        }}
        initGraph();
    </script>
    </html>
    """
    with open(f"{name}.html", "w") as file:
        file.write(html_content)
    print(f"Done making {name}.html")

    print(f"\nCongratz, you've made a desmos art")
    print(f"The result is in {name}.html")
    print(f"Open it in your favorite browser!")

if __name__ == "__main__":
    """
    This is the main function to run the program.
    """
    # Get all image files in the current directory
    image_files = get_image_files()
    if len(image_files) == 0:
        print("No image found")
        exit()

    # Select an image from the list
    img_dir = select_image(image_files)
    img = cv.imread(img_dir)
    if img is None:
        print("Error: Failed to read image file.")
        exit()

    # Apply a Gaussian blur to the image
    img = cv.GaussianBlur(img, (5, 5), 1.4)

    # Apply Canny edge detection
    canny = apply_canny_edge_detection(img)

    while True:
        # Get the name for the output
        name = input("\nName for the output: ")
        if not name:
            print("Error: Please enter a valid file name.")
            continue

        # Check if the name contains invalid characters
        if not name.replace('.', '', 1).replace('_', '').isalnum():
            print("Error: File name contains invalid characters.")
            continue

        # Check if the name is a reserved name
        if name in ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']:
            print("Error: File name is a reserved name.")
            continue

        # Check if the file exists
        if os.path.exists(name + '.bmp') or os.path.exists(name + '.svg'):
            print(f"File {name} will be overwrite!")

        break

    # Generate the output files
    generate_output_files(canny, name)