from constant import  ANSWER_MARKS, NUM_OPTIONS
from utils import preprocess_sheet,  find_bubble_contours, preprocess_bubble
import cv2
from bubble_classifier import bubble_classifier


def recognize_bubble_sheet(img):
    # Preprocess the image and find contours
    preprocessed_img = preprocess_sheet(img)
    contours = find_bubble_contours(preprocessed_img)

    # Recognize each bubble
    bubble_results = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        offset = 10
        x, y, w, h = max(x - offset, 0), max(y - offset, 0), w + 2 * offset, h + 2 * offset
        w, h = min(w, img.shape[1] - x), min(h, img.shape[0] - y)
        cropped_image = img[y:y+h, x:x+w]

        preprocessed_bubble = preprocess_bubble(cropped_image)
        result = bubble_classifier(preprocessed_bubble)

        if result["label"] != "invalid":
            bubble_results.append({"label": result["label"], "result": result, "x": x, "y": y, "w": w, "h": h})
            
    # Sort bubbles by coordinates
    bubbles_sorted = sorted(bubble_results, key=lambda b: (b["y"], b["x"]))

    # Organize the bubbles into stacks
    bubble_stacks = []
    i = 0

    while i < len(bubbles_sorted):
        row_candidate = bubbles_sorted[i:i + NUM_OPTIONS]
        row_sorted = [bubble for j, bubble in enumerate(row_candidate) if abs(row_candidate[0]["y"] - bubble["y"]) <= 10]

        bubble_stacks.append(row_sorted)
        i += len(row_sorted)

    # Sort each stack by x-coordinate
    bubble_stacks_sorted = [sorted(stack, key=lambda b: b["x"]) for stack in bubble_stacks]

    # Fill the gaps in bubble stacks
    for i in range(NUM_OPTIONS):
        lowest_x = None

        for stack in bubble_stacks_sorted:
            if len(stack) > i:
                current_x = stack[i]["x"]
                if lowest_x is None or current_x < lowest_x:
                    lowest_x = current_x

        if lowest_x is None:
            continue

        for stack in bubble_stacks_sorted:
            if len(stack) < i + 1:
                prev = stack[i - 1]
                stack.insert(i, {"label": "unknown", "result": None, "x": lowest_x, "y": prev["y"], "h": prev["h"], "w": prev["w"]})
            else:
                current = stack[i]
                gap = current["x"] - lowest_x
                if gap > 20:
                    stack.insert(i, {"label": "unknown", "result": None, "x": lowest_x, "y": current["y"], "h": current["h"], "w": current["w"]})

    # Interpret the marks
    marks = []

    for stack in bubble_stacks_sorted:
        mark = 'not filled'

        for i, bubble in enumerate(stack):
            if bubble["label"] == 'unknown':
                mark = 'uncertain'
                break
            if bubble["label"] in ['crossed', 'filled']:
                if mark != 'not filled':
                    mark = 'invalid'
                else:
                    mark = ANSWER_MARKS[i]

        marks.append(mark)

    labels = [[item["label"] for item in sublist] for sublist in bubble_stacks_sorted]
    full_result = [[item["result"] for item in sublist] for sublist in bubble_stacks_sorted]

    return {"marks": marks, "labels": labels, "full_result": full_result}