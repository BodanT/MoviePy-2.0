import os
import argparse
import json
import re
from moviepy.editor import ColorClip, ImageClip, VideoFileClip, TextClip, CompositeVideoClip, clips_array, concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from datetime import datetime

ImageMagick_dir = os.getcwd() + "\\portablePython\\python310\\Tools\\ImageMagick\\bin"
print("Image Magick Directory:", ImageMagick_dir)

#On windows for some reason it cannot find ImageMagic binary, so we need to tell MoviePy where it is
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": ImageMagick_dir + r"\\magick.exe"})
#change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.0.8-Q16\\magick.exe"})

def remove_comments(text):
    # Remove single-line comments (// ...) from the text
    text = re.sub(r'\/\/[^\n]*', '', text)
    return text
	
def parse_time(time_str):
    # Parse time in HH:MM:SS.MMM format and return it in seconds
    time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1000000

def add_text_to_video(video_path, text_elements, output_path):
    txt_clips = []
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    
    for element in text_elements:
        start_time = parse_time(element["start_time"])
        end_time = parse_time(element["end_time"])
        text = TextClip(element["text"], fontsize=element["font_size"], color=element["color"])
        text = text.set_start(start_time)
        text = text.set_duration(end_time - start_time)
        text = text.set_position((int(element["position_x"]),int(element["position_y"])))
        txt_clips.append(text)
    	
    #Save video
    final_video = CompositeVideoClip([video_clip] + txt_clips)
    final_video.write_videofile(output_path, codec=None)
    #final_video.write_videofile(output_path, codec='libx264')

def add_title_and_end_screen(video_path, start_title, end_title, output_path):
    title_duration = parse_time("00:00:05.000")
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Create a text clip with the title for the beginning of the video
    start_text_clip = TextClip(start_title, fontsize=70, color='black')
    start_text_clip = start_text_clip.set_duration(title_duration)

    # Create a text clip with the title for the end of the video
    end_text_clip = TextClip(end_title, fontsize=70, color='black')
    end_text_clip = end_text_clip.set_duration(title_duration)

    # Create a color clip with black background and white text, with a duration of 5 seconds
    color_clip = ColorClip(video_clip.size, color=(255, 255, 255), duration=title_duration)

    # Create an image clip from the provided image file
    image_clip = ImageClip("files/fri_logo.png", duration=title_duration)
    # Resize the image to a smaller width, maintaining the original aspect ratio
    new_width = 350  # Set the desired width (adjust as needed)
    image_clip = image_clip.resize(width=new_width)

    # Calculate the new height to maintain the aspect ratio
    aspect_ratio = image_clip.size[0] / image_clip.size[1]
    new_height = int(new_width / aspect_ratio)

    # Position the resized image clip at the bottom right
    image_x = video_clip.size[0] - new_width
    image_y = video_clip.size[1] - new_height
    image_clip = image_clip.set_position((image_x, image_y))

    # Overlay the text clip on the color clip
    start_text_overlay_clip = CompositeVideoClip([color_clip, start_text_clip.set_position('center')])
    end_text_overlay_clip = CompositeVideoClip([color_clip, end_text_clip.set_position('center')])

    # Overlay the image clip on both start and end screens
    start_text_overlay_clip = CompositeVideoClip([start_text_overlay_clip, image_clip])
    end_text_overlay_clip = CompositeVideoClip([end_text_overlay_clip, image_clip])


    # Concatenate the video clip with the text clip
    final_clip = concatenate_videoclips([start_text_overlay_clip, video_clip, end_text_overlay_clip])
    # Save the video
    final_clip.write_videofile(output_path, codec='libx264')


def main():

    # parser = argparse.ArgumentParser(description='Add text to a video using MoviePy')
    # parser.add_argument('-c', '--config', required=True, help='Path to the JSON configuration file')
    # parser.add_argument('-i', '--input', required=True, help='Path to the input video file')
    # parser.add_argument('-o', '--output', required=True, help='Path to the output video file')
    # args = parser.parse_args()

    # # Read the JSON configuration file and remove comments
    # with open(args.config, 'r') as config_file:
    #     config_text = remove_comments(config_file.read())
    #     config = json.loads(config_text)
    #     text_elements = config.get("text_elements", [])

    # add_text_to_video(args.input, text_elements, args.output)
    add_title_and_end_screen("files/input.mp4", "Hello World", "GoodBye World",  "files/out1.mp4")
    
    

if __name__ == '__main__':
    main()