def get_objects(box, class_id):
    if box.cls == class_id:
        return box.xywh[0].cpu().numpy()
    return None

def get_white_balls(results):
    white_balls = []
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if box.cls == 4:  # Assuming class ID 4 is for the white balls
                    white_balls.append(box.xywh[0].cpu().numpy())  # Append the bounding box coordinates
    return white_balls