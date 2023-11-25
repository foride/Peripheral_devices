import cv2
import imutils
from pygrabber.dshow_graph import FilterGraph


def print_cameras():
    graph = FilterGraph()
    devices = graph.get_input_devices()
    if devices:
        print("Available input devices:")
        for index, device in enumerate(devices, start=0):
            print(f"{index}. {device}")
    else:
        print("No input devices found.")
    camera_chose = int(input())
    return camera_chose


def set_camera_properties(camera, width=None, height=None):
    if width is not None:
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    if height is not None:
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def capture_photo(photo_path='photo.jpg', width=640, height=480):
    # Open the camera

    camera_index = print_cameras()
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    set_camera_properties(cap, width, height)

    brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    contrast = cap.get(cv2.CAP_PROP_CONTRAST)
    saturation = cap.get(cv2.CAP_PROP_SATURATION)

    while True:

        # Capture a frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't read frame.")
            break

        # Display the frame
        cv2.imshow('Camera Feed', frame)

        print(
            f"Current Camera Properties - Width: {width}, Height: {height},"
            f" Brightness: {brightness}, Contrast: {contrast}, Saturation: {saturation}")

        key_pressed = cv2.waitKey(30)
        if key_pressed == ord("q"):
            break
        elif key_pressed == ord('w'):  # Increase brightness
            brightness += 10
            cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        elif key_pressed == ord('s'):  # Decrease brightness
            brightness -= 10
            cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        elif key_pressed == ord('e'):  # Decrease contrast
            contrast -= 10
            cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        elif key_pressed == ord('d'):  # Increase contrast
            contrast += 10
            cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        elif key_pressed == ord('r'):  # Decrease saturation
            saturation -= 10
            cap.set(cv2.CAP_PROP_SATURATION, saturation)
        elif key_pressed == ord('f'):  # Increase saturation
            saturation += 10
            cap.set(cv2.CAP_PROP_SATURATION, saturation)
        if key_pressed == ord("p"):
            # Save the photo
            cv2.imwrite(photo_path, frame)

            # Release the camera
            cap.release()
            print(f"Photo captured and saved to {photo_path}")


def capture_video(video_path='video.avi', duration_seconds=10, width=640, height=480):
    camera_index = print_cameras()
    # Open the camera
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    set_camera_properties(cap, width, height)

    # Get the default camera properties
    brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    contrast = cap.get(cv2.CAP_PROP_CONTRAST)
    saturation = cap.get(cv2.CAP_PROP_SATURATION)

    while True:

        # Capture a frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't read frame.")
            break

        # Display the frame
        cv2.imshow('Camera Feed', frame)

        print(
            f"Current Camera Properties - Width: {width}, Height: {height},"
            f" Brightness: {brightness}, Contrast: {contrast}, Saturation: {saturation}")

        key_pressed = cv2.waitKey(30)
        if key_pressed == ord("q"):
            break
        elif key_pressed == ord('w'):
            brightness += 10
            cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        elif key_pressed == ord('s'):
            brightness -= 10
            cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        elif key_pressed == ord('e'):
            contrast -= 10
            cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        elif key_pressed == ord('d'):
            contrast += 10
            cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        elif key_pressed == ord('r'):
            saturation -= 10
            cap.set(cv2.CAP_PROP_SATURATION, saturation)
        elif key_pressed == ord('f'):
            saturation += 10
            cap.set(cv2.CAP_PROP_SATURATION, saturation)
        if key_pressed == ord("p"):

            # Define the codec and create a VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (width, height))

            # Capture video for the specified duration
            start_time = cv2.getTickCount()
            while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < duration_seconds:
                ret, frame = cap.read()
                if not ret:
                    break

                # Write the frame to the video file
                out.write(frame)

            # Release the camera and video writer
            cap.release()
            out.release()
            print(f"Video captured and saved to {video_path}")


def motion_detection():
    camera_index = print_cameras()
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    _, start_frame = cap.read()
    start_frame = imutils.resize(start_frame, width=500)
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_RGB2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

    alarm = False
    alarm_mode = False
    alarm_counter = 0

    while True:

        _, frame = cap.read()
        frame = imutils.resize(frame, width=500)

        if alarm_mode:
            frame_bw = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

            difference = cv2.absdiff(frame_bw, start_frame)
            threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
            start_frame = frame_bw

            if threshold.sum() > 300:
                alarm_counter += 1
            else:
                if alarm_counter > 0:
                    alarm_counter -= 1

            cv2.imshow("Cam", threshold)
        else:
            cv2.imshow("Cam", frame)

        if alarm_counter > 20:
            if not alarm:
                alarm = True
                print("Motion detected!")
                for _ in range(5):
                    if not alarm_mode:
                        break
                    print("ALARM")
                alarm = False

        key_pressed = cv2.waitKey(30)
        if key_pressed == ord("t"):
            alarm_mode = not alarm_mode
            alarm_counter = 0
        if key_pressed == ord("q"):
            alarm_mode = False
            break

    cap.release()
    cv2.destroyAllWindows()


def menu():
    while True:
        print("Input:")
        print("0. Motion Detection")
        print("1. Capture Photo")
        print("2. Capture Video")
        print("3. Exit")

        choice = input("Enter your choice (0-3): ")

        if choice == "0":
            motion_detection()
        elif choice == "1":
            photo_name = input("Enter photo name: ")
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            capture_photo(photo_name, width, height)
        elif choice == "2":
            video_name = input("Enter video file name: ")
            duration_seconds = int(input("Enter duration (in seconds): "))
            width = int(input("Enter width: "))
            height = int(input("Enter height: "))
            capture_video(video_name, duration_seconds, width, height)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 3.")


if __name__ == "__main__":
    menu()
