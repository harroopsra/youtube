import praw
import requests
from pathlib import Path
import subprocess
import os
from config import CLIENT_ID, CLIENT_SECRET, USER_AGENT, PASSWORD, USERNAME
import random
import re

def save_images(subreddit_name = "ArtPorn"):
    reddit = praw.Reddit(
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        password = PASSWORD,
        user_agent= USER_AGENT,
        username = USERNAME
        )

    Path(str(Path.cwd())+f"/{subreddit_name}").mkdir(exist_ok=True)

    count = 0
    names = []

    with open(f"titles{subreddit_name}.txt","w") as f:          # Clean titles from previous runs
        f.write("")
    for post in reddit.subreddit(f"{subreddit_name}").top(time_filter="day",limit=6):
        url = post.url
        print(url)
        file_extension = url.split('.')[-1]
        print(file_extension)
        if url.endswith("png") or url.endswith("jpg") or url.endswith("jpeg"):
            count += 1
            response = requests.get(url)
            with open(f"{subreddit_name}/{str(count).zfill(3)}.{file_extension}","wb") as f:
                f.write(response.content)
            with open(f"titles{subreddit_name}.txt","a") as f:
                f.write(post.title + "\n")


def get_sorted_image_paths(directory):
    image_paths = [file for file in os.listdir(directory) if file.endswith('.jpeg') or file.endswith('.png')]
    sorted_image_paths = sorted(image_paths, key=lambda x: int(x.lstrip('changed_keyframe').rstrip('.jpeg').rstrip('.png')))
    sorted_image_paths = [os.path.join(directory, path) for path in sorted_image_paths]
    return sorted_image_paths

def build_video(names, image_paths:list,duration=2,transition_duration=0.5,output_fname="output.mp4",add_text=False):

    """
    # Builds out a video when given 
    1. image paths in a list, 
    2. image duration (default = 2)
    3. transition duration(default = 0.5)
    4. output file name (default = "output.mp4")
    """

    transition_list = ['fade', 'wipeleft', 'wiperight', 'wipeup', 'wipedown', 'slideleft', 'slideright', 'slideup', 'slidedown', 'circlecrop', 'rectcrop', 'distance', 'fadeblack', 'fadewhite', 'radial', 'smoothleft', 'smoothright', 'smoothup', 'smoothdown', 'circleopen', 'circleclose', 'vertopen', 'vertclose', 'horzopen', 'horzclose', 'dissolve', 'pixelize', 'diagtl', 'diagtr', 'diagbl', 'diagbr', 'hlslice', 'hrslice', 'vuslice', 'vdslice', 'hblur', 'fadegrays', 'wipetl', 'wipetr', 'wipebl', 'wipebr', 'squeezeh', 'squeezev', 'zoomin']

    command = 'ffmpeg -y -hide_banner \\\n'

    for i,path in enumerate(image_paths):
        command += f'-i {path} \\\n'

    command += f'-ss \'{random.choice(range(200))}\' -i sounds/chopin.m4a \\\n'

    command +=  ' -filter_complex "\\\n'

    for i in range(len(image_paths)):
        #names[i] = re.sub('"','',names[i])
        #names[i] = re.sub("'","",names[i])
        #text = f",drawtext=text=\'{names[i].strip()}\':fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=30:box=1:boxcolor=white:boxborderw=40:fontcolor=black:x=(w-text_w)/2:y=h-150"
        if not add_text:
            text = ""
        command += f'[{i}]scale=w=1080:h=ih*1080/iw,pad=\'1080:1920:(ow-iw)/2:(oh-ih)/2\',scale=w=4000:h=ih*4000/iw,zoompan=z=\'zoom+0.001\':x=\'iw/2-iw/zoom/2\':y=\'ih/2-ih/zoom/2\':d=100:s=1080x1920{text},format=yuv420p[p{i}]; \\\n'

    #global because we need it for map
    i = 0
    while i<(len(image_paths)-1):    
        if i==0:
            command += f'[p{i}][p{i+1}]xfade=transition={random.choice(transition_list)}:duration={transition_duration}:offset={(i+1)*duration}[f{i}]; \\\n'
        else:
            command += f'[f{i-1}][p{i+1}]xfade=transition={random.choice(transition_list)}:duration={transition_duration}:offset={(i+1)*duration}[f{i}]; \\\n'
        
        i+=1

    command += '" \\\n'

    command += f'-map "[f{i-1}]" -map {len(image_paths)}:a:0 -t {len(image_paths)*(duration)}  -pix_fmt yuv420p  -vcodec libx264 -preset ultrafast {output_fname}'

    print(command)

    subprocess.call(command, shell=True)
    print("Video created")


def remove_files_from_dir(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

"""
subreddit_name = "streetart"

save_images(subreddit_name)

images = get_sorted_image_paths(subreddit_name)
with open("titles.txt","r") as f:
    names = f.readlines()

build_video(names,images,1,0.4,"output.mp4",add_text=False)
"""

for subreddit in ["ArtPorn","Art","museum"]:
    remove_files_from_dir(subreddit)           # Delete remnants from previous steps
    save_images(subreddit)

    images = get_sorted_image_paths(subreddit)
    with open(f"titles{subreddit}.txt","r") as f:
        names = f.readlines()

    build_video(names,images,1.25,0.25,f"output{subreddit}.mp4",add_text=False)


# TODO

# Might be worth checking out ways to automate writing descritpions and titles (probably gpt4) when titles are given

# Write a function that processes all the images to make them 1080 by 1920
# This bypasses the padding step
# Essentially write your own padding instead of relying on ffmpeg because for an image that is already 1080 by 1920, ffmpeg breaks down. The alternative is to scale to a different number but have the same aspect ratio as 1080 x 1920