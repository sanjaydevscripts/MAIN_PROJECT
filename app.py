# from flask import Flask, render_template, request, jsonify
# import os  # Import os for file handling
# from flask_cors import CORS  # Import CORS
# from ultralytics import YOLO
from flask import Flask, render_template, request, jsonify
import os  # Import os for file handling
from flask_cors import CORS  # Import CORS
from ultralytics import YOLO
import cv2
import numpy as np
import shutil

app = Flask(__name__)
CORS(app)  # ✅ Apply CORS AFTER defining app

UPLOAD_FOLDER = r'C:/Users/Hp/Desktop/MAIN_PROJECT2025/static/image/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # ✅ Create folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

#analyse
@app.route('/analyse', methods=['POST'])
def analyse_image():
    print("Received request")  # Debugging print
    data = request.get_json()  # Get JSON data from frontend

    if not data or "img_src" not in data:
        return jsonify({"error": "No image source provided"}), 400

    img_src = data["img_src"]
    print(f"Image source received: {img_src}")  # Debugging print

    try:
        model = YOLO("model.pt")
        
        input_image_path = f"C:/Users/Hp/Desktop/MAIN_PROJECT2025/static/enhance_image/{img_src}"  # Replace with your image path
        output_dir = "C:/Users/Hp/Desktop/MAIN_PROJECT2025/static/predict_image"    
        temp_subfolder = os.path.join(output_dir, "predict")          # Specify the directory to save the image
        model.predict(
            source=input_image_path,
            show=True,
            save=True,
            conf=0.6,
            line_width=1,
            project=output_dir,  # Custom output directory
            name=""  # Folder name inside 'predict_out'
        )
        #print("value--------",value)
        if os.path.exists(temp_subfolder):
            for file in os.listdir(temp_subfolder):
                shutil.move(os.path.join(temp_subfolder, file), output_dir)  # Move files
            os.rmdir(temp_subfolder)  # Remove the empty 'predict' folder
        value =  f"http://127.0.0.1:5000/static/predict_image/{img_src}"
        return jsonify({"path": value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#enhance    
@app.route('/enhance', methods=['POST'])
def enhance_image():
    print("Received request")  # Debugging print
    data = request.get_json()  # Get JSON data from frontend

    if not data or "img_src" not in data:
        return jsonify({"error": "No image source provided"}), 400

    img_src = data["img_src"]
    print(f"Image source received: {img_src}")  # Debugging print

    try:
       
        input_image_path = f"C:/Users/Hp/Desktop/MAIN_PROJECT2025/static/image/{img_src}"  # Replace with your image path
        output_dir = "C:/Users/Hp/Desktop/MAIN_PROJECT2025/static/enhance_image/"              # Specify the directory to save the image
        enhance_and_save_image(input_image_path, output_dir,img_src)



        value =  f"http://127.0.0.1:5000/static/enhance_image/{img_src}"
        #print("value--------",value)
        return jsonify({"path": value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)  # ✅ Save file to the folder

    print(f'File saved: {file_path}')  # Debugging

    return jsonify({'message': f'File uploaded: {file.filename}'}), 200

@app.route('/delete_all', methods=['POST'])
def delete_all_files():
    """Delete all images in image, enhance_image, and predict_image folders."""
    folders = [
        "C:/Users/Hp/Desktop/MAIN_PROJECT2025/static/image/",
        "C:/Users/Hp/Desktop/MAIN_PROJECT2025/static/enhance_image/",
        "C:/Users/Hp/Desktop/MAIN_PROJECT2025/static/predict_image/"
    ]

    try:
        for folder in folders:
            if os.path.exists(folder):
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)  # Delete file
                print(f"All files deleted from {folder}")  # Debugging

        return jsonify({'message': 'All images deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Delete Image Route
@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.get_json(force=True, silent=True)  # ✅ Handle JSON safely

    if not data or 'filename' not in data:
        return jsonify({'error': 'No filename provided'}), 400

    filename = data['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    print(f'Trying to delete: {file_path}')  # Debugging

    if os.path.exists(file_path):
        os.remove(file_path)  # ✅ Delete file
        print(f'File deleted: {file_path}')
        return jsonify({'message': f'File {filename} deleted'}), 200
    else:
        print(f'File not found: {file_path}')
        return jsonify({'error': 'File not found'}), 404

def enhance_and_save_image(input_path, output_directory, output_filename="enhanced_image.jpg"):
    # Load the image using the input path
    image = cv2.imread(input_path)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load the image from {input_path}")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Resize for consistent processing (optional)
    resized_image = cv2.resize(image, (600, 400))

    # 1. Adjust contrast only (Remove brightness adjustment)
    alpha = 1.5  # Contrast control (1.0-3.0)
    enhanced_image = cv2.convertScaleAbs(resized_image, alpha=alpha)

    # 2. Apply sharpening filter
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    enhanced_image = cv2.filter2D(enhanced_image, -1, kernel)

    # Save the final enhanced image
    output_path = os.path.join(output_directory, output_filename)
    cv2.imwrite(output_path, enhanced_image)

    print(f"Image enhancement complete. Enhanced image saved at: {output_path}")


if __name__ == '__main__':
    app.run(debug=True)
