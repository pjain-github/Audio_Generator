import cv2
import os
import tempfile

class VideoReverser:

    def __init__(self):
        pass

    def reverse_video(self, input_path, output_path="reversed_output.mp4", temp=True):
        # Open the video file
        cap = cv2.VideoCapture(input_path)

        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

        # Store frames in a list
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()

        # Reverse the frame order
        frames.reverse()

        if temp:
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            output_path = temp_file.name

        # Save the reversed video
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        for frame in frames:
            out.write(frame)

        out.release()
        print(f"Reversed video saved to {output_path}")

        return output_path

# Usage
if __name__=='__main__':
    rev = VideoReverser()
    rev.reverse_video("input.mp4", "reversed_output.mp4", temp=False)