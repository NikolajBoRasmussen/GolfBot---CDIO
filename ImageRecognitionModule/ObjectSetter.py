from ObjectGetter import get_objects, get_white_balls
def set_objects(objects):
    cross = None
    egg = None
    robot = None
    orange_ball = None
    white_balls = None

    for object in objects:
        for box in object.boxes:
            match box.cls:
                case 0:
                    if cross is not None:
                        if (cross[3] < get_objects(box, 0)[3] and cross[2] < get_objects(box, 0)[2]):
                            cross = get_objects(box, 0)
                    else:
                        cross = get_objects(box, 0)
                case 1:
                    if egg is not None:
                        if (egg[3] < get_objects(box, 1)[3] and egg[2] < get_objects(box, 1)[2]):
                            egg = get_objects(box, 1)
                    else:
                        egg = get_objects(box, 1)
                case 2:
                    orange_ball = get_objects(box, 2)
                case 3:
                    if robot is not None:
                        if (robot[3] < get_objects(box, 3)[3] and robot[2] < get_objects(box, 3)[2]):
                            robot = get_objects(box, 3)
                    else:
                        robot = get_objects(box, 3)
                case 4:
                    white_balls = get_white_balls(objects)

    return cross, egg, robot, orange_ball, white_balls