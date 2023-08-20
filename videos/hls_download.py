# import requests as r
# import m3u8 as mn
# import subprocess
# import time

# def main():
#     with open('video.ts','wb') as f:
#         a = 8756
#         while True:
#             url = f"https://live-cf.cdn.hotstar.com/hls/live/2024726/inallow-icc-wtc2023/hin/1540023548/15mindvrm01965f3b31530049bd859d7f7eb410a39608june2023/master_1_0{a}.ts"
#             a = a+1
#             print(url)
#             a_c = r.get(url)
#             f.write(a_c.content)
#             # time.sleep(4)
#             if a==8800:
#                 break
#     subprocess.run(['ffmpeg','-i','video.ts','video.mp4'])
#     print('done')

# main()
import requests as r
import m3u8 as mn
import subprocess

def main(value):
    a_a = r.get(value)
    a_b = mn.loads(a_a.text)
    with open('video.ts','wb') as f:
        for s in a_b.data['segments']:
            url = 'https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-eu-west-1-prod/bb762bf3-8927-424b-b490-810f719e4e51/'+str(s['uri'])
            print(url)
            a_c = r.get(url)
            f.write(a_c.content)
    subprocess.run(['ffmpeg','-i','video.ts','video.mp4'])
    print('done')

main("https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-eu-west-1-prod/bb762bf3-8927-424b-b490-810f719e4e51/default.jobtemplate.hls360.m3u8")