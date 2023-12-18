import subprocess

def srt_mv():
    command = ' ffmpeg -i "' + "uploaded.mp4" + '" -lavfi ' + '"subtitles=' + 'output.srt' + ':force_style=' + "'BorderStyle=0,Outline=1,Shadow=0,Fontsize=18'" + '"' + ' -y -crf 1 -c:a copy "' + "output.mp4" + '"'
    subprocess.call(command, shell=True)