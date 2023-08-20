import subprocess
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

video  = ffmpeg_streaming.input('C:/Users/MURALI/Desktop/store/venv/ecomm/media/videos/test4/video.mp4')

_480 = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))

hls = video.hls(Formats.h264(), hls_list_size=8, hls_time=5)
hls.flags('delete_segments')
hls.representations(_480)
hls.output('C:/Users/MURALI/Desktop/store/venv/ecomm/media/videos/test4/master.m3u8')