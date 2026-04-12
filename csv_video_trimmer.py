'''
Copyright (c) 2026 Michael Medina <mike0012@protonmail.ch>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import csv
import os
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

def trim_video(original_video, csv_trims):
    with open(csv_trims, mode='r') as file:
        video_edits = csv.DictReader(file)
        video_names_counter = {}
        group_dict = {}
        for idx, video_edit in enumerate(video_edits):
            start_time = video_edit.get('start_time', "").strip()
            end_time = video_edit.get('end_time', "").strip()
            output_video = video_edit.get('output_video','output_video_'+str(idx + 1)).strip()
            output_video_temp = output_video.replace(' ', "\\ ")
            group = video_edit.get('group', '').strip()
            if group:
                group = int(group)
            if (not output_video_temp in video_names_counter) and (not group in group_dict):
                video_names_counter[output_video_temp] = 1
                if group:
                    output_video_temp = f"{output_video_temp}_{video_names_counter[output_video_temp]}"
                    group_dict[group] = [output_video_temp]
            else:
                if not output_video_temp in video_names_counter:
                    video_names_counter[output_video_temp] = 1
                else:
                    video_names_counter[output_video_temp] += 1
                output_video_temp = f"{output_video_temp}_{video_names_counter[output_video_temp]}"
                if group:
                    group_dict[group].append(output_video_temp)
            if start_time and end_time:
                # originally set to subprocess.run(f"ffmpeg -i {original_video} -ss {start_time} -to {end_time} -c copy {output_video_temp}.mp4", shell=True) but resulted in black video frames for first 2 seconds and frozen frames on video merge
                # below transcodes the trimmed video which takes longer than copying but fixes black frames for first 2 seconds
                subprocess.run(f"ffmpeg -i {original_video} -ss {start_time} -to {end_time} -c:v libx264 -crf 18 -preset slow -c:a copy {output_video_temp}.mp4", shell=True)
            elif start_time:
                subprocess.run(f"ffmpeg -i {original_video} -ss {start_time} -c:v libx264 -crf 18 -preset slow -c:a copy {output_video_temp}.mp4", shell=True)
            elif end_time:
                subprocess.run(f"ffmpeg -i {original_video} -to {end_time} -c copy {output_video_temp}.mp4", shell=True)
            else:
                pass
        for group in group_dict.keys():
            file = open("video_list.txt", "w")
            file.write("")
            file.close()
            output_video_of_group = group_dict[group][0][:-2]
            file = open("video_list.txt", "a")
            for counter, video in enumerate(group_dict[group]):
                print(f"Group: {group}, video: {video}")
                video_path = video.replace("\\","")
                video_path = Path(f"{video}.mp4").resolve()
                video_path = str(video_path).replace("\\", "")
                file.write(f"file '{video_path}'")
                if counter != len(group_dict[group]) - 1:
                    file.write("\n")
            file.close()
            subprocess.run(f"ffmpeg -f concat -safe 0 -i video_list.txt -c copy {output_video_of_group}.mp4", shell=True)
            for video in group_dict[group]:
                video_name = video.replace("\\","")
                os.remove(f"{video_name}.mp4")
        os.remove("video_list.txt")

            

if __name__ == '__main__':
    start_time = datetime.now()
    parser = argparse.ArgumentParser(prog='csv_video_trimmer.py')
    parser.add_argument('-v', '--video', required=True, help="This is the video that will be used for creating video trims/cuts, this video MUST be mp4 format!")
    parser.add_argument('-f', '--file', required=True, help="This is the csv file that will assist in creating video trims/cuts videos. Must have columns: output_video, start_time, end_time and group. start_time and end_time must be formatted: HH:mm:ss")
    args = parser.parse_args()
    original_video = args.video
    csv_trims = args.file
    trim_video(original_video, csv_trims)
    end_time = datetime.now()
    print(f"The program took {(end_time - start_time).total_seconds()} seconds")
