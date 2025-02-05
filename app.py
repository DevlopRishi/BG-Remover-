from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64, re
from io import BytesIO
from PIL import Image

app = Flask(__name__)

def readb64(base64_string):
    """Convert base64 image string to an OpenCV image (numpy array)."""
    img_data = re.sub('^data:image/.+;base64,', '', base64_string)
    img_bytes = base64.b64decode(img_data)
    pil_img = Image.open(BytesIO(img_bytes)).convert("RGBA")
    # Convert to OpenCV format (BGR with alpha)
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
    return cv_img

def convert_to_base64(cv_img):
    """Convert an OpenCV image to a base64-encoded PNG."""
    success, buffer = cv2.imencode('.png', cv_img)
    if not success:
        return None
    b64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/png;base64,{b64}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_auto', methods=['POST'])
def process_auto():
    # Get image from the POSTed JSON data.
    data = request.json.get('image')
    img = readb64(data)
    if img is None:
        return jsonify({'error': 'Invalid image data'}), 400

    # Create an initial mask using a rectangle nearly covering the entire image.
    mask = np.zeros(img.shape[:2], np.uint8)
    height, width = img.shape[:2]
    rect = (10, 10, width - 20, height - 20)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Pixels marked as definite or probable foreground
    mask2 = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')
    result = cv2.bitwise_and(img, img, mask=mask2)
    result_b64 = convert_to_base64(result)
    return jsonify({'result': result_b64})

@app.route('/process_manual', methods=['POST'])
def process_manual():
    # Get both the original image and the manual mask (from the overlay canvas).
    image_data = request.json.get('image')
    mask_data = request.json.get('mask')
    img = readb64(image_data)
    mask_overlay = readb64(mask_data)  # This image should have an alpha channel indicating painted areas.
    if img is None or mask_overlay is None:
        return jsonify({'error': 'Invalid image or mask data'}), 400

    # Use the alpha channel from the manual mask (if any) to mark definite foreground.
    if mask_overlay.shape[2] == 4:
        alpha = mask_overlay[:, :, 3]
    else:
        alpha = cv2.cvtColor(mask_overlay, cv2.COLOR_BGR2GRAY)
    manual_mask = np.full(img.shape[:2], cv2.GC_PR_BGD, dtype=np.uint8)
    manual_mask[alpha > 0] = cv2.GC_FGD

    # Create an initial GrabCut mask from a rectangle.
    mask = np.zeros(img.shape[:2], np.uint8)
    height, width = img.shape[:2]
    rect = (10, 10, width - 20, height - 20)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Override mask values using the manual mask.
    mask[manual_mask == cv2.GC_FGD] = cv2.GC_FGD
    cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)
    mask2 = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')
    result = cv2.bitwise_and(img, img, mask=mask2)
    result_b64 = convert_to_base64(result)
    return jsonify({'result': result_b64})

if __name__ == '__main__':
    app.run(debug=True)
