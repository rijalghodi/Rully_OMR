import cv2
import numpy as np

def resize_with_padding(img, target_size=(224, 224), padding_color=(255, 255, 255)):
    """
    Resize image with no changing aspect ration but adding padding
    
    Args:
    img (ndarray): Input image in BGR format.
    
    Returns:
    ndarray: Resized image.
    """
    h, w = img.shape[:2]
    target_h, target_w = target_size

    # Calculate the scaling factor to maintain the aspect ratio
    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)

    # Resize the image to the new dimensions
    resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Create a new image with the target size and the padding color
    new_img = np.full((target_h, target_w, 3), padding_color, dtype=np.uint8)

    # Calculate the position to place the resized image
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2

    # Place the resized image onto the new image
    new_img[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_img

    return new_img

def preprocess_bubble(img):
    """
    Preprocesses the bubble image by converting it to grayscale, applying Gaussian blur,
    applying adaptive thresholding, and then resizing it
    
    Args:
    img (ndarray): Input image in BGR format.
    
    Returns:
    ndarray: Thresholded image.
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    # img = cv2.GaussianBlur(img, (3, 3), 1)  # Apply Gaussian blur
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    #                                cv2.THRESH_BINARY, 225, 30)  # Apply adaptive thresholding
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Convert image to bgr
    img = resize_with_padding(img, (224, 224))
    return img

def preprocess_sheet(img):
    """
    Preprocesses the sheet image by converting it to grayscale, applying Gaussian blur,
    and then applying adaptive thresholding.
    
    Args:
    img (ndarray): Input image in BGR format.
    
    Returns:
    ndarray: Thresholded image.
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    img = cv2.GaussianBlur(img, (3, 3), 1)  # Apply Gaussian blur
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 225, 20)  # Apply adaptive thresholding
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Convert image to grayscale
    return img

def is_contour_circular(contour):
    """
    Determines if a contour is circular based on its perimeter and bounding rectangle's aspect ratio.
    
    Args:
    contour (ndarray): Contour to be checked.
    
    Returns:
    bool: True if the contour is circular, False otherwise.
    """
    perimeter = cv2.arcLength(contour, True)
    if perimeter == 0:
        return False

    x, y, w, h = cv2.boundingRect(contour)
    circularity = (3.14159 * w) / perimeter
    aspect_ratio = w / float(h)
    
    return 0.8 < aspect_ratio < 1.2 and 0.7 < circularity < 1.3  # Circularity and aspect ratio thresholds

def find_bubble_contours(img):
    """
    Finds and filters contours in the thresholded image based on aspect ratio and circularity.
    
    Args:
    img (ndarray): Thresholded image.
    
    Returns:
    list: List of valid contours.
    """

    _, input_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(input_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print(contours)
    # contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # Find all contours
    
    valid_contours = []

    # cv2.drawContours(contour_img, contours, -1, (0, 0, 255), 2)

    # cv2.imshow('all contours', contour_img)
    # cv2.waitKey(0)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Ensure h is not zero to avoid division by zero
        if h == 0:
            continue
        
        aspect_ratio = w / float(h)
        area = cv2.contourArea(contour)
        
        # Filter out contours with inappropriate aspect ratio or too small area
        if not (0.5 < aspect_ratio < 1.5 and area >= 300):
            continue
        
        # Potential check for circular contours
        # if is_contour_circular(contour):
        # valid_contours.append({"contour": contour, "x": x, "y": y, "w": w, "h": h})
        valid_contours.append(contour)

    return valid_contours

def draw_contours(img, contours, color=(0, 255, 0), thickness=2):
    """
    Draws contours on the image.
    
    Args:
    img (ndarray): Original image.
    contours (list): List of contours to be drawn.
    color (tuple): Color of the contours.
    thickness (int): Thickness of the contour lines.
    
    Returns:
    ndarray: Image with contours drawn.
    """
    cv2.drawContours(img, contours, -1, color, thickness)
    return img
