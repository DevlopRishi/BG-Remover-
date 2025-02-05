
# Background Remover Web App

This project is a web-based background removal application that uses OpenCV's GrabCut algorithm for automatic segmentation and allows manual refinement via an interactive painting interface. Users can upload an image, automatically remove its background, and further adjust the result by "painting" corrections on an overlay. The application is built using Flask for the backend and HTML5/JavaScript for the frontend.

## Features

- **Automatic Background Removal:**  
  Uses OpenCV's GrabCut algorithm to automatically segment the foreground from the background.

- **Manual Refinement:**  
  Provides a canvas overlay for users to manually paint corrections. Users can adjust:
  - Brush size
  - Opacity
  - Hardness (as a placeholder for future enhancements)
  - Eraser mode (to remove manual markings)

- **Real-Time Feedback:**  
  View the processed image immediately after applying automatic or manual segmentation.

## File Structure
BG-Remover/
├── app.py
└── templates/
    └── index.html

- **app.py:**  
  The Flask backend application. It defines endpoints for automatic background removal (`/process_auto`) and for applying the manual mask (`/process_manual`).

- **templates/index.html:**  
  The frontend interface which contains:
  - An image upload control.
  - Two canvas elements (one for displaying the image and one for the painting overlay).
  - Controls to adjust brush parameters and toggle the eraser.
  - Buttons to send the image data to the backend for processing.

## Requirements

- Python 3.6 or higher
- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/) (using `opencv-python-headless` is recommended for environments without a display)
- [NumPy](https://numpy.org/)
- [Pillow](https://python-pillow.org/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/background_remover.git
   cd background_remover
   ```

2. **(Optional) Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Linux/macOS
   venv\Scripts\activate       # On Windows
   ```

3. **Install the required packages:**

   ```bash
   pip install flask opencv-python-headless numpy pillow
   ```

## Running the Application

1. **Start the Flask server:**

   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**

   ```
   http://localhost:5000
   ```

## How to Use

1. **Upload an Image:**  
   Click the file input to select an image. The image will be displayed on the background canvas.

2. **Manual Painting:**  
   Use the overlay canvas to paint corrections. Adjust the brush size, opacity, and hardness via the provided sliders. Use the "Toggle Eraser" button to switch between painting and erasing modes.

3. **Automatic Background Removal:**  
   Click the "Auto Remove Background" button to run GrabCut with a default rectangular segmentation.

4. **Apply Manual Mask:**  
   After making manual corrections, click the "Apply Manual Mask" button. This sends both the original image and the manual mask to the backend, where GrabCut is re-run to refine the segmentation.

5. **View Results:**  
   The processed image will be displayed below the controls.

## Future Improvements

- Implement a more advanced hardness setting for brush strokes.
- Allow users to specify separate markings for foreground and background.
- Add undo/redo functionality for manual corrections.
- Improve error handling and user feedback.
- Deploy the application on a production server.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [OpenCV](https://opencv.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Pillow](https://python-pillow.org/)
```
