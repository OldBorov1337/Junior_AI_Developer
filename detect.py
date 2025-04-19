import cv2
import mediapipe as mp
import json
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("input_video", type=str)
parser.add_argument("output_json", type=str)
args = parser.parse_args()

input_path = args.input_video
output_json_path = args.output_json
output_video_path = os.path.splitext(output_json_path)[0] + "_with_skeleton.mp4"

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

cap = cv2.VideoCapture(input_path)

if not cap.isOpened():
    print("Failed to open video:", input_path)
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

output_data = []
frame_num = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    frame_data = {"frame": frame_num, "keypoints": {}}

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            frame_data["keypoints"][mp_pose.PoseLandmark(idx).name.lower()] = [
                round(landmark.x, 5),
                round(landmark.y, 5),
                round(landmark.visibility, 5)
            ]

    output_data.append(frame_data)
    out_video.write(frame)
    frame_num += 1

cap.release()
out_video.release()

with open(output_json_path, 'w') as f:
    json.dump(output_data, f, indent=2)

print("Done")
