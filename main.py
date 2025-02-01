import cv2 as cv
import os
import subprocess

def callback(input):
    pass

if __name__ == "__main__":
    dct = {}
    count = 0
    for file in os.listdir():
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
            count += 1
            dct[count] = file
    if count == 0:
        print("No image found")
        exit()
    print("List of image in this folder:")
    for index, file in dct.items():
        print(f"{index}: {file}")
    while True:
        index = input(f"Choose one of it (1{' - ' + str(len(dct)) if len(dct) > 1 else ''}): ")
        try:
            img_dir = dct[int(index)]
            break
        except:
            print("Invalid index")

    img = cv.imread(img_dir)
    img = cv.GaussianBlur(img, (5, 5), 1.4)

    cv.namedWindow('canny')
    cv.createTrackbar("minThres", 'canny', 0, 255, callback)
    cv.createTrackbar("maxThres", 'canny', 0, 255, callback)
    print("\nSlide or input the minThres and maxThres values")
    print("Click 'q' if you are done with the settings")
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        min_thres = cv.getTrackbarPos('minThres', 'canny')
        max_thres = cv.getTrackbarPos('maxThres', 'canny')
        canny = cv.Canny(img, min_thres, max_thres)
        cv.imshow('canny', canny)

    cv.destroyAllWindows()
    name = ""
    while True:
        try:
            name = input("Name for the output: ")
            if len(name) > 0:
                break
        except Exception as e:
            print("ERROR:")
            print(e)
            exit()
    print(f"\nMaking {name}.bmp")
    cv.imwrite(f"{name}.bmp", canny)
    print(f"Done making {name}.bmp")

    print(f"\nRunning potrace --svg {name}.bmp -o {name}.svg")
    subprocess.run(["potrace", "--svg", f"{name}.bmp", "-o", f"{name}.svg"], check=True)
    print(f"Done running potrace --svg {name}.bmp -o {name}.svg")