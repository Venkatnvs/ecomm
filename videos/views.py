from django.shortcuts import render

# Create your views here.
def main(request):
    url = "https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-eu-west-1-prod/ea2b28c0-0c87-4dd1-af14-c704a9c74ea8/default.jobtemplate.hls.m3u8"
    return render(request, 'videos/video_play.html')

def main2(request):
    return render(request, 'player/main.html')

def main3(request):
    return render(request, 'videos/video_play2.html')

def ctm_play(request):
    return render(request, 'videos/ctm/index.html')