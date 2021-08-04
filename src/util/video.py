import cv2

def create_output_video_writer(video, filepath, slowness=1):
    fps = int(video.get(cv2.CAP_PROP_FPS) / slowness)
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    video_writer = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
    return video_writer

