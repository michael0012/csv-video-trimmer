# CSV Video Trimmer

A brief, one-sentence description of what this Python script does and the problem it solves.

## 🚀 Getting Started

### Prerequisites
* Python 3.x
* ffmpeg

### Usage:
python csv_video_trimmer.py -v <video_name> -f <csv_name>
- Video (REQUIRED!!): This is the video that will be used for creating video trims/cuts, this video MUST be mp4 format!
- CSV file (REQUIRED!!): This is the csv file that will assist in creating video trims/cuts videos. Must have columns: output_video, start_time, end_time and group. start_time and end_time must be formatted: HH:mm:ss, group must be a whole number greater than zero and output_video is the name of the video clip, which should be non-empty
- both must be in the same folder as the python script
