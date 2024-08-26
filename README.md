## Overview

The Virtual Mouse project allows users to control their computer's mouse cursor and simulate mouse clicks using hand gestures captured by a webcam. The application uses the MediaPipe library for hand tracking and PyAutoGUI for mouse control.

## Features

- **Mouse Movement**: Move the cursor based on the position of the index finger.
- **Mouse Click**: Simulate a mouse click when the index and middle fingers are close together.
- **FPS Display**: Shows the current frames per second (FPS) on the video feed.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## Installation

1. **Clone the repository** (if applicable) or download the source code.

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

4. **Install the required packages**:

   ```bash
   pip install opencv-python mediapipe pyautogui numpy
   ```

## Usage

1. **Run the application**:

   ```bash
   python main.py
   ```

2. **Control the virtual mouse**:

   - **Mouse Movement**: Move the cursor by positioning your index finger.
   - **Mouse Click**: Click by bringing your index and middle fingers close together.

3. **Exit the application**: Press `q` while the application window is focused.

## Troubleshooting

- **Missing Libraries**: Ensure all required libraries are installed. Refer to the `Installation` section for details.
- **Camera Issues**: Ensure your webcam is properly connected and accessible.
- **Permission Issues**: Ensure the script has permission to access the webcam and control the mouse.

## Contributing

Feel free to fork the repository and make improvements. If you encounter issues or have suggestions, please open an issue or submit a pull request.


## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for hand tracking.
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for mouse control.
- [OpenCV](https://opencv.org/) for image processing.


