Automating the creation of YouTube shorts and forcing myself to become more cultured at the same time

# YouTube Shorts
## _Or how I forced myself to be more cultured_

Examples: https://www.youtube.com/@ArtForItsOwnSake

## Features

Given a subreddit name, this program:
- Sources images and their titles using the Python Reddit API Wrapper or [PRAW](https://praw.readthedocs.io/en/stable/)
    - Creates a directory for each reddit where it stores the downloaded images
    - Creates a text file for each reddit where it stores the titles called titles{subreddit_name}.txt
- Uses a downloaded copy of Chopin because he's cultured (and mostly because he's non-copyrighted) for music from [here](https://www.youtube.com/watch?v=F5hhdLUuLB0) using [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Creates a string which is a valid  [ffmpeg](https://ffmpeg.org/) command that can:
    - piece together all the image files that have been downloaded
        - First, you scale each image so that it's width is 1080, then you pad the remaining height (we want 1080 by 1920 for phones) with black rectangles, then you scale these images to an insane number because you want to zoom-in slowly and it looks really bizarre if you don't scale, then you resize so that the image is again 1080 by 1920, and then you stich them all up
    - If required, add the titles of each post to the video
        - using the drawtext filter
- Then it uses the subprocess module to call the ffmpeg command setting shell as True
    - This generates an output .mp4 video that I upload

I run the above in a for loop for 4 different subreddits, namely "ArtPorn","Art","museum" and "minimalism_art"

Example of a generated command (slightly shorter since we set add_text as False):
```
ffmpeg -y -hide_banner \
-i museum/001.jpeg \
-i museum/002.png \
-i museum/003.jpeg \
-i museum/004.jpeg \
-i museum/005.jpeg \
-i museum/006.jpeg \
-ss '136' -i sounds/chopin.m4a \
 -filter_complex "\
[0]scale=w=1080:h=ih*1080/iw,pad='1080:1920:(ow-iw)/2:(oh-ih)/2',scale=w=4000:h=ih*4000/iw,zoompan=z='zoom+0.001':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=100:s=1080x1920,format=yuv420p[p0]; \
[1]scale=w=1080:h=ih*1080/iw,pad='1080:1920:(ow-iw)/2:(oh-ih)/2',scale=w=4000:h=ih*4000/iw,zoompan=z='zoom+0.001':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=100:s=1080x1920,format=yuv420p[p1]; \
[2]scale=w=1080:h=ih*1080/iw,pad='1080:1920:(ow-iw)/2:(oh-ih)/2',scale=w=4000:h=ih*4000/iw,zoompan=z='zoom+0.001':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=100:s=1080x1920,format=yuv420p[p2]; \
[3]scale=w=1080:h=ih*1080/iw,pad='1080:1920:(ow-iw)/2:(oh-ih)/2',scale=w=4000:h=ih*4000/iw,zoompan=z='zoom+0.001':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=100:s=1080x1920,format=yuv420p[p3]; \
[4]scale=w=1080:h=ih*1080/iw,pad='1080:1920:(ow-iw)/2:(oh-ih)/2',scale=w=4000:h=ih*4000/iw,zoompan=z='zoom+0.001':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=100:s=1080x1920,format=yuv420p[p4]; \
[5]scale=w=1080:h=ih*1080/iw,pad='1080:1920:(ow-iw)/2:(oh-ih)/2',scale=w=4000:h=ih*4000/iw,zoompan=z='zoom+0.001':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=100:s=1080x1920,format=yuv420p[p5]; \
[p0][p1]xfade=transition=smoothup:duration=0.2:offset=1.1[f0]; \
[f0][p2]xfade=transition=vertclose:duration=0.2:offset=2.2[f1]; \
[f1][p3]xfade=transition=circlecrop:duration=0.2:offset=3.3000000000000003[f2]; \
[f2][p4]xfade=transition=vertclose:duration=0.2:offset=4.4[f3]; \
[f3][p5]xfade=transition=slideright:duration=0.2:offset=5.5[f4]; \
" \
-map "[f4]" -map 6:a:0 -t 6.6000000000000005  -pix_fmt yuv420p  -vcodec libx264 -preset ultrafast outputmuseum.mp4
```

I then upload these videos online

Examples can be seen on my channel: https://www.youtube.com/@ArtForItsOwnSake
