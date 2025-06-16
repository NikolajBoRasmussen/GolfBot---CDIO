import cv2

cap = cv2.VideoCapture(1)  # try with 1 as well if needed

if not cap.isOpened():
    print("❌ Could not open camera.")
else:
    print("✅ Camera opened successfully.")
    ret, frame = cap.read()
    if ret:
        print("✅ Frame captured.")
        cv2.imshow("Test", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("❌ Failed to read from camera.")
    cap.release()
