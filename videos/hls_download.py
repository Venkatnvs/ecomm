import requests as r
import m3u8 as mn
import subprocess

def main(value):
    a_a = r.get(value)
    a_b = mn.loads(a_a.text)
    with open('video.ts','wb') as f:
        for s in a_b.data['segments']:
            url = 'https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-eu-west-1-prod/ea2b28c0-0c87-4dd1-af14-c704a9c74ea8/'+str(s['uri'])
            print(url)
            a_c = r.get(url)
            f.write(a_c.content)
    subprocess.run(['ffmpeg','-i','video.ts','video.mp4'])
    print('done')

main("https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-eu-west-1-prod/ea2b28c0-0c87-4dd1-af14-c704a9c74ea8/default.jobtemplate.hls480.m3u8")