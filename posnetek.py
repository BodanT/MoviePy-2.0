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

def format_duration(duration):
    duration = int(duration) # Convert to seconds
    hours, mins, secs = duration // 3600, (duration % 3600) // 60, duration % 60
    return f"{hours:02d}:{mins:02d}:{secs:02d}"

def add_title_and_end_screen(video_path, title_of_video, title_of_next_video, subtitle, output_path):
    title_duration = parse_time("00:00:05.000")
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Create/get all the text needed to be added to the clips
    theme="Naslov: "+title_of_video
    duration_txt = "Trajanje:"
    duration_str = format_duration(video_clip.duration + title_duration * 2)
    subtitle="Podnaslov: " + subtitle
    lea="LAPSy Embedded Academy"
    next_video="Naslednji posnetek: "+title_of_next_video
    end_title = "Hvala za ogled!"

    #get the custom font (Right now is the font that the university uses)
    custom_font="fonts/garamond.ttf"

    # Create a text clip with the title for the beginning of the video
    theme_clip=TextClip(theme, fontsize=70, color='black', font=custom_font).set_duration(title_duration).set_position(('center')).set_start(0)
    subtitle_clip=TextClip(subtitle, fontsize=35, color='black', font=custom_font).set_duration(title_duration).set_position(('center', video_clip.h/2+50)).set_start(0)
    professor_clip=TextClip(duration_txt, fontsize=35, color='black', font=custom_font).set_duration(title_duration).set_position((5, video_clip.size[1]-85)).set_start(0)
    duration_clip=TextClip(duration_str, fontsize=35, color='black', font=custom_font).set_duration(title_duration).set_position((10, video_clip.size[1]-50)).set_start(0)
    lea_clip=TextClip(lea, fontsize=50, color='white', font=custom_font).set_duration(title_duration).set_position(('center', 30)).set_start(0)
    next_video_clip=TextClip(next_video, fontsize=35, color='black', font=custom_font).set_duration(title_duration).set_position(('center', 420)).set_start(0)

    # Create a text clip with the title for the end of the video
    end_text_clip = TextClip(end_title, fontsize=70, color='black', font=custom_font).set_duration(title_duration).set_position('center')

    # Create a color clip with black background and white text, with a duration of 5 seconds
    color_clip = ColorClip(video_clip.size, color=(255, 255, 255), duration=title_duration)
    red_lane = ColorClip((video_clip.size[0], 100), color=(180, 22, 44), duration=title_duration).set_position(('center', 0)).set_start(0)

    # Create an image clip from the provided image file
    fri_logo_clip = ImageClip("photos/fri_logo.png", duration=title_duration)
    lea_logo_clip= ImageClip("photos/lea.png", duration=title_duration)
    # Resize the image to a smaller width, maintaining the original aspect ratio
    new_width = 300  # Set the desired width (adjust as needed)
    fri_logo_clip = fri_logo_clip.resize(width=new_width)
    lea_logo_clip= lea_logo_clip.resize(height=100)
    lea_logo_clip = lea_logo_clip.set_position((0,0))

    # Calculate the new height to maintain the aspect ratio
    aspect_ratio = fri_logo_clip.size[0] / fri_logo_clip.size[1]
    new_height = int(new_width / aspect_ratio)

    # Calculate the x-position for the right bottom corner
    image_x = video_clip.size[0] - new_width
    image_y = video_clip.size[1] - new_height
    fri_logo_clip = fri_logo_clip.set_position((image_x, image_y))

    # Overlay the text clip on the color clip
    start_text_overlay_clip = CompositeVideoClip([color_clip, red_lane, professor_clip, duration_clip, theme_clip, subtitle_clip, lea_clip, lea_logo_clip, fri_logo_clip])
    end_text_overlay_clip = CompositeVideoClip([color_clip, red_lane, end_text_clip, fri_logo_clip, lea_logo_clip, next_video_clip, lea_clip])

    # Concatenate the video clip with the text clip
    final_clip = concatenate_videoclips([start_text_overlay_clip, video_clip, end_text_overlay_clip])
    # Save the video
    final_clip.write_videofile(output_path, codec='libx264')


def edit_all_videos(folder_path, output_path, config_path):
    # Read the JSON configuration file and remove comments
    with open(config_path, 'r') as config_file:
        config_text = remove_comments(config_file.read())
        config = json.loads(config_text)
        text_elements = config.get("spica", [])

    #Go through all elements in the config file and edit the videos
    for element in text_elements:
        #Get the video name and the text elements
        video_name = element.get("video_name", "")
        title_of_video = element.get("title_of_video", "")
        title_of_next_video = element.get("title_of_next_video", "")
        subtitle= element.get("subtitle", "")
        place=element.get("place", "")
        cut=element.get("cut", "")

        #Create the paths to the input and output videos and temp video
        video_path = os.path.join(folder_path, f"{video_name}.mp4")
        output_video_path = os.path.join(output_path, f"{video_name}_edited.mp4")
        temp_video_path = os.path.join(output_path, f"{video_name}_temp.mp4")

        #Check if the video exists and edit it
        if os.path.exists(video_path):
            print(f"Editing video: {video_name}")
            if(place=="None"):
                #add title and end screen
                add_title_and_end_screen(video_path, title_of_video, title_of_next_video, subtitle, output_video_path)
            else:
                # hide all the people in the video
                hide_people(video_path, temp_video_path, place, cut)
                # make temporaty video with the title screen and end screen
                add_title_and_end_screen(temp_video_path, title_of_video, title_of_next_video, subtitle, output_video_path)

                # remove the temporary video
                os.remove(temp_video_path)
            print(f"Done editing video: {video_name}")
        else:
            print(f"Video not found: {video_name}")




def hide_people(video_path, output_path, position, start_time):

    video = VideoFileClip(video_path)
    k = video.duration

    if start_time != 0:
        cut_video = CompositeVideoClip([video.subclip(start_time, k)])
        k=cut_video.duration
        banner = ImageClip("photos/"+ position + ".jpg").set_position(position, position).set_duration(k).set_start(0)
        final = CompositeVideoClip([cut_video, banner])
        final.write_videofile(output_path, codec="libx264")
    else:
        banner = ImageClip("photos/" + position + ".jpg").set_position(position, position).set_duration(k).set_start(0)
        final = CompositeVideoClip([video, banner])
        final.write_videofile(output_path, codec="libx264")

    VideoFileClip(video_path).close()


def main():


    # edit_all_videos("input", "output", "spica.json")


    parser = argparse.ArgumentParser(description='Add text to a video using MoviePy')
    parser.add_argument('-c', '--config', required=True, help='Path to the JSON configuration file')
    parser.add_argument('-i', '--input', required=True, help='Path to the input video file')
    parser.add_argument('-o', '--output', required=True, help='Path to the output video file')
    args = parser.parse_args()

    edit_all_videos(args.input, args.output, args.config)

    
    

if __name__ == '__main__':
    main()