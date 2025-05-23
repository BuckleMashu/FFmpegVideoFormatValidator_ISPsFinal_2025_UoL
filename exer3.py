# %% [markdown]
# ffmpeg-python and ffprobe-python are wrapper libraries (make it easier to use those tools from within Python code. They depend on the actual ffmpeg and ffprobe executables being present on your system), 
# 
# so they will still need the ffmpeg and ffprobe installed in the PC and linked in Path.

# %%
%pip install ffmpeg-python

# %% [markdown]
# tasks:
# 1) ffprobe to examine video files
# 2) identify which files do not adhere to the video format guidelines. Which includes:
#     - Video format (container): mp4
#     - Video codec: h.264
#     - Audio codec: aac
#     - Frame rate: 25 FPS
#     - Aspect ratio: 16:9
#     - Resolution: 640 x 360
#     - Video bit rate: 2 – 5 Mb/s
#     - Audio bit rate: up to 256 kb/s
#     - Audio channels: stereo
# 3) convert the videos to be along the guidelines via ffmpeg, and add '_fortmatOK' at the end of the name
# 

# %%
import ffmpeg
from fractions import Fraction
import os

def check_vid_format(title,checklist,check_boxes):
    i = len(title)-1
    while i >= 0:
        if title[i] == ".":
            vid_format = title[i+1:]
            break
        i-=1
    if vid_format != checklist["vid_format"]:
        check_boxes[0] = False
    return check_boxes,vid_format

def check_vid_codec(source,checklist,check_boxes):
    codec = source[0]["codec_name"]
    if codec != checklist["video_codec"]:
        check_boxes[1] = False
    return check_boxes,codec

def check_audio_codec(source,checklist,check_boxes):
    codec = source[1]["codec_name"]
    if codec != checklist["audio_codec"]:
        check_boxes[2] = False
    return check_boxes,codec

def check_vid_frame_rate(source,checklist,check_boxes):
    frame_raw = source[0]['r_frame_rate']
    i = len(frame_raw)-1
    while i >=0:
        if frame_raw[i] == "/":
            frame_rate = int(frame_raw[:i]) / int(frame_raw[i+1:])
            break
        i-=1
    if round(frame_rate) != checklist["frame_rate"]:
        check_boxes[3] = False
    return check_boxes,round(frame_rate)

def check_aspect_ratio(source,checklist,check_boxes):
    out = None
    if "display_aspect_ratio" in source[0]:
        if source [0]["display_aspect_ratio"] != checklist["aspect_ratio"]:
            check_boxes[4] = False
            out = source [0]["display_aspect_ratio"]
    else:
        numerator = source[0]["width"]
        denominator = source[0]["height"]
        fraction = Fraction(numerator, denominator)
        ar = str(fraction.numerator) + ":" + str(fraction.denominator)
        if ar != checklist["aspect_ratio"]:
            check_boxes[4] = False
            out = ar
    return check_boxes, out

def check_resolutions(source,checklist,check_boxes):
    w = source[0]["width"]
    h = source[0]["height"]
    if str(w)+"x"+str(h) != checklist["resolution"]:
        check_boxes[5] = False
    return check_boxes, str(w)+"x"+str(h)

def check_video_bit_rate(source,checklist,check_boxes):
    bit_rate = int(source[0]["bit_rate"])/1000000
    if checklist["v_bit_r_min"] > bit_rate or bit_rate > checklist["v_bit_r_max"]:
        check_boxes[6] = False
    return check_boxes, bit_rate

def check_audio_bit_rate(source,checklist,check_boxes):
    if int(source[1]["bit_rate"])/1000 > checklist["a_bit_r_max"]:
        check_boxes[7] = False
    return check_boxes, int(source[1]["bit_rate"])/1000

def check_audio_channel(source,checklist,check_boxes,channels_layout):
    out = None
    if "channel_layout" in source[1]:
        if source[1]["channel_layout"] != checklist["channels"]:
            check_boxes[8] = False 
            out = source[1]["channel_layout"]
    else:
        if channels_layout[source[1]["channels"]] != checklist["channels"]:
            check_boxes[8] = False
            out = channels_layout[source[1]["channels"]]
    return check_boxes, out

def convert_video(titles_outcome, correct_settings):
    for title, checks in titles_outcome.items():
        options = {}
        for i, requirement in enumerate(checks):
            if requirement == False:
                things_to_add = correct_settings[i]
                for changes in things_to_add:
                    options[changes[0]] = changes[1]

        i,j = len(title) - 1,len(title) - 1
        format_found = False
        while i >= 0:
            if format_found == False and title[i] == '.':
                j = i
                format_found = True
            if format_found == True and title[i] == "/":
                output_file =  "./Exercise3_Films_formatOK/" + title[i+1:j] + "_formatOK.mp4"
                break
            i -= 1

        print(output_file)
        print(options)
        #command = ffmpeg.input(title).output(output_file, **options)
        #print("FFmpeg Command:", command.compile()) # This line should now also run if the function is entered
        try:
            (
                ffmpeg
                .input(title)
                .output(output_file, **options)
                .run(overwrite_output=True, quiet=False)
            )
            print(f"Successfully converted '{title}' to '{output_file}'")
        except ffmpeg.Error as e:
            print(f"FFmpeg error encoding '{title}': {e.stderr.decode()}")
        except Exception as e:
            print("Exception: ", e)
        pass

entries = os.listdir('./Exercise3_Films')
print(entries)
titles = []
titles_output = []
for title in entries:
    titles.append("./Exercise3_Films/"+title)
    titles_output.append("./Exercise3_Films_formatOK/"+title)
print(titles)
print(titles_output)
print("---------------------------------------------")

video_checklist = {"vid_format":"mp4","video_codec":"h264","audio_codec":"aac","frame_rate":25,
                   "aspect_ratio":"16:9","resolution":"640x360","v_bit_r_min":2, 
                   "v_bit_r_max":5, "a_bit_r_max":256,"channels":"stereo"}

channels_layout = {1:"mono",2:"stereo",3:"2.1",4:"quad",6:"5.1",8:"7.1"}

titles_outcome = {}
txt_content = ""
for i,title in enumerate(titles):
    check_boxes = [True,True,True,True,True,True,True,True,True]
    issues = [None,None,None,None,None,None,None,None,None]
    txt_content = txt_content + title + "'s issue(s) found:\n"
    check_boxes,issues[0] = check_vid_format(title,video_checklist,check_boxes)
    meta_datas = ffmpeg.probe(title)["streams"]
    check_boxes,issues[1] = check_vid_codec(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[2] = check_audio_codec(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[3] = check_vid_frame_rate(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[4] = check_aspect_ratio(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[5] = check_resolutions(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[6] = check_video_bit_rate(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[7] = check_audio_bit_rate(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[8] = check_audio_channel(meta_datas,video_checklist,check_boxes,channels_layout)
    if check_boxes[1] == False or check_boxes[3] == False or check_boxes[4] == False or check_boxes[5] == False:
        if check_boxes[6] == True:
            issues[6] = "Converting the video will modify the bit rate"
        check_boxes[6] = False
    print(check_boxes)
    requirements = list(video_checklist.keys())
    for x,check in enumerate(check_boxes):
        if check == False:
            if x == 6:
                if isinstance(issues[x],str):
                    txt_content = txt_content + "   special condition: " + issues[x]+"\n"
                else:
                    txt_content = txt_content + "   input: " + str(issues[x])+ " | requirement's "+" video bit range"+" : " + "2-5"+"\n"
            elif x > 6:
                txt_content = txt_content + "   input: " + str(issues[x])+ " | requirement's "+requirements[x+1]+" : " + str(video_checklist[requirements[x+1]])+"\n"
            else:
                txt_content = txt_content + "   input: " + str(issues[x])+ " | requirement's "+requirements[x]+" : " + str(video_checklist[requirements[x]])+"\n"
    titles_outcome[title] = check_boxes
    txt_content = txt_content + "\n"

print(titles_outcome)
with open("Submissions'_problems_report.txt", 'w', encoding='utf-8') as f:
    f.write(txt_content)
print("---------------------------------------------")
correct_settings = [[['f','mp4']],[['c:v','libx264']],[['c:a','aac']],
                    [['r',25]],[['vf','scale=640:360,setsar=1:1']],[['vf','scale=640:360,setdar=16/9']],
                    [['b:v','3M'],['minrate','2M'],['maxrate','5M'],['bufsize','6M']],[['b:a','256k']],[['ac',2]]]

convert_video(titles_outcome,correct_settings)

# %%
#checking of the formats are correct
entries_checking = os.listdir('./Exercise3_Films_formatOK')
titles_checking = []
for title in entries_checking:
    titles_checking.append("./Exercise3_Films_formatOK/"+title)

titles_outcome = {}
for i,title in enumerate(titles_checking):
    check_boxes = [True,True,True,True,True,True,True,True,True]
    check_boxes,issues[0] = check_vid_format(title,video_checklist,check_boxes)
    meta_datas = ffmpeg.probe(title)["streams"]
    check_boxes,issues[1] = check_vid_codec(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[2] = check_audio_codec(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[3] = check_vid_frame_rate(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[4] = check_aspect_ratio(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[5] = check_resolutions(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[6] = check_video_bit_rate(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[7] = check_audio_bit_rate(meta_datas,video_checklist,check_boxes)
    check_boxes,issues[8] = check_audio_channel(meta_datas,video_checklist,check_boxes,channels_layout)
    print(check_boxes)
    print(issues[4])
    print(issues[6])
    titles_outcome[title] = check_boxes


# %% [markdown]
# Reference:
# 1) Abdeladim Fadheli (2024) Extract Media Metadata in Python. Available at: https://thepythoncode.com/article/extract-media-metadata-in-python (Accessed: 11 february 2025).
# 2) Josephine Loo (2023) How to Use FFmpeg in Python with Examples. Available at: https://www.bannerbear.com/blog/how-to-use-ffmpeg-in-python-with-examples/ (Accessed: 11 February 2025).
# 3) FFmpeg (no date) FFmpeg Documentation. Available at: https://ffmpeg.org/ffmpeg.html (Accessed: 12 February 2025).
# 4) GeeksforGeeks (2024) Python | List files in a directory. Available at: https://www.geeksforgeeks.org/python-list-files-in-a-directory/ (Accessed: 13 February 2025).
# 


