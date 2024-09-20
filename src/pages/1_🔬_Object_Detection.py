from io import BytesIO
import streamlit as st
import cv2
from PIL import Image, ImageOps
import numpy as np
from collections import Counter

from configs.config import CLASSES, COLORS, DEFAULT_CONFIDENCE_THRESHOLD, MODEL, PROTOTXT

@st.cache_data
def process_image(image):
    """
    Pre-process an image for object detection using the MobileNet SSD model.

    Parameters:
    image (np.ndarray): The input image in the form of a NumPy array.

    Returns:
    np.ndarray: The detections returned by the MobileNet SSD model.
    """
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5
    )
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
    net.setInput(blob)
    detections = net.forward()
    return detections

@st.cache_data
def annotate_image(
    image, detections, confidence_threshold=DEFAULT_CONFIDENCE_THRESHOLD, show_boxes=True
):
    """
    Annotate an image with bounding boxes and labels based on object detection results.

    Parameters:
    image (np.ndarray): The input image in the form of a NumPy array.
    detections (np.ndarray): The object detections returned by the MobileNet SSD model.
    confidence_threshold (float): Minimum confidence threshold for displaying detections.
    show_boxes (bool): Whether to draw bounding boxes around detected objects.

    Returns:
    Tuple[np.ndarray, list]: The annotated image and a list of labels for detected objects.
    """
    (h, w) = image.shape[:2]
    labels = []
    if show_boxes:
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > confidence_threshold:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                label = f"{CLASSES[idx]}: {round(confidence * 100, 2)}%"
                labels.append(label)
                cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(
                    image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2
                )
    return image, labels

@st.cache_data
def convert_image_to_bytes(image):
    """
    Convert a PIL image to a bytes object for download.

    Parameters:
    image (PIL.Image.Image): The PIL image to be converted.

    Returns:
    bytes: The image in PNG format as a bytes object.
    """
    img_buffer = BytesIO()
    image.save(img_buffer, format="PNG")  # Save the PIL image as PNG to the buffer
    img_bytes = img_buffer.getvalue()  # Get the binary content
    return img_bytes

st.title("Object detection with MobileNet SSD")

st.markdown(
    """
    This application demonstrates real-time object detection using the MobileNet SSD (Single Shot Multibox Detector) model. 
    It allows users to upload images and process them through a deep learning model that detects various objects, 
    including people, animals, vehicles, and more.

    - **Upload an Image:** Users can upload a PNG, JPG, or JPEG image for object detection.
    - **Confidence Threshold:** Adjust the minimum confidence level for detected objects.
    - **Bounding Boxes:** Toggle to display or hide bounding boxes around detected objects.
    - **Image Augmentation:** Apply basic augmentations such as flipping, rotating, and resizing the input image before detection.

    Once processed, you can download the annotated image and review a summary of the detected objects.
    """
)

# File uploader for images
img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Slider for confidence threshold
confidence_threshold = st.slider(
    "Confidence threshold", 0.0, 1.0, DEFAULT_CONFIDENCE_THRESHOLD, 0.05
)

# Check to display bounding boxes or not
show_boxes = st.checkbox("Show bounding boxes", value=True)

# Image Augmentation Options
augment_option = st.radio("Apply image augmentation", ["None", "Flip", "Rotate", "Resize"])

if img_file_buffer is not None:
    # Image Processing Logic
    image = np.array(Image.open(img_file_buffer))

    # Apply augmentations
    if augment_option == "Flip":
        image = ImageOps.mirror(Image.fromarray(image))
    elif augment_option == "Rotate":
        angle = st.slider("Select rotation angle", 0, 360, 0)
        image = Image.fromarray(image).rotate(angle)
    elif augment_option == "Resize":
        new_size = st.slider("Select new size", 100, 1000, 300)
        image = cv2.resize(image, (new_size, new_size))

    # Process image and annotate
    detections = process_image(np.array(image))
    image, labels = annotate_image(np.array(image), detections, confidence_threshold, show_boxes)

    # Display image with annotations
    st.image(image, caption="Processed Image", use_column_width=True)

    # Display list of detected objects
    st.write(labels)

    # Display object count summary
    label_counts = Counter([label.split(":")[0] for label in labels])
    st.write(f"Object Summary: {dict(label_counts)}")

    # Display confidence distribution
    confidences = [float(label.split(":")[1][:-1]) for label in labels]
    if confidences:
        st.bar_chart(confidences)

    # Option to download the annotated image
    # Convert the annotated image to bytes
    annotated_img_pil = Image.fromarray(image)
    annotated_img_bytes = convert_image_to_bytes(annotated_img_pil)

    # Create a download button
    st.download_button("Download image", annotated_img_bytes, file_name="annotated_image.png")
