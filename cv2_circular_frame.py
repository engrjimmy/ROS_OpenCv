import cv2

def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        height, width, channels = frame.shape
        center_x, center_y = int(width/2), int(height/2)

        circule_scaling = 0.5

        if width <height:
            radius = int(width * circule_scaling /2 )
        else:
            radius = int(height * circule_scaling/2)
        cv2.circle(frame, (center_x, center_y), radius, (0, 100, 0), 2)
        cv2.imshow("Circular Frame", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()