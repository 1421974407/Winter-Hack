# Report for Winter Hack Code

**Author:** Jian Zhao

## Introduction

This document outlines my code designed to detect laser pointers in video frames captured from a camera using the OpenCV library. The system is capable of identifying laser pointers of different colors and estimating the confidence and their distance from the camera, with a potential range of up to two meters in dark conditions.

## Main Functionality

The primary function of this script is to detect laser pointers and display their color, distance, and confidence level on the video frame. The rendering show is as below:

![Code Rendering](image-url)  *Fig1. Code rendering*

## Performance

### Dark Conditions

In dark conditions, the system can effectively detect laser pointers up to two meters away. The contrast between the laser light and the dark background enhances the detection accuracy.

### Complex Lighting Conditions

In environments with complex lighting, such as rooms with various light sources, the detection can be challenging due to interference and noise. I try to use morphological operations and Gaussian blurring to mitigate these issues but maybe not enough in practical cases.

## Implementation Method

1. **Camera Initialization**: The script starts by initializing the default camera using `cv2.VideoCapture(0)`.

2. **Color Space Conversion**: Each frame is converted from BGR to HSV color space, which is more suitable for color-based image segmentation.

3. **Color Thresholding**: The script defines specific HSV ranges for red, green, and blue colors. It applies these ranges to create masks that isolate the colors of the laser pointers.

4. **Morphological Operations**: To refine the masks and remove noise, the script applies an opening operation using `cv2.morphologyEx` with a kernel of size 5x5.

5. **Gaussian Blurring**: A Gaussian blur is applied to the mask to further smooth out the image and reduce noise.

6. **Contour Detection**: The script uses `cv2.findContours` to detect contours in the blurred mask. These contours represent the shapes of the laser spots.

7. **Laser Spot Analysis**: For each contour, the script calculates the area and uses it along with color purity to estimate a confidence score. This score helps in filtering out false detections.

8. **Distance Estimation**: The script estimates the distance of the laser pointer from the camera based on the size of the detected spot. The formula used is an inverse relationship between the radius and the distance, which is calibrated for accuracy.

9. **Display**: The detected laser pointers are marked with a circle, and their details (color, distance, and confidence) are displayed on the video frame.

Please replace `image-url` with the actual URL or path to the image file that you want to display. If the image is located in the same directory as the Markdown file, you can simply use the image filename.
