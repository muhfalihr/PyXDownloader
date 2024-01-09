import re
data_videos = [
    {
        "bitrate": 256000,
        "content_type": "video/mp4",
        "url": "https://video.twimg.com/ext_tw_video/1703423935470239744/pu/vid/avc1/488x270/SywNdsUY3uJFAftB.mp4?tag=12"
    },
    {
        "bitrate": 832000,
        "content_type": "video/mp4",
        "url": "https://video.twimg.com/ext_tw_video/1703423935470239744/pu/vid/avc1/720x398/BBnJ8wSqeLcW410m.mp4?tag=12"
    },
    {
        "content_type": "application/x-mpegURL",
        "url": "https://video.twimg.com/ext_tw_video/1703423935470239744/pu/pl/nGfj1LPSUlF3wuxR.m3u8?tag=12&container=fmp4&v=9c9"
    }
]


# video_tertinggi = max(
#     data_videos, key=lambda x: x.get('bitrate', 0), default=None)

# if video_tertinggi:
#     print(video_tertinggi.get('url'))
# else:
#     print(None)


def ambil_nama_file_dari_url(url):
    pola = r'/([^/?]+)\?'
    hasil = re.search(pola, url)
    if hasil:
        return hasil.group(1)
    else:
        return None


# Contoh penggunaan
url = "https://video.twimg.com/ext_tw_video/1703423935470239744/pu/vid/avc1/720x398/BBnJ8wSqeLcW410m.mp4?tag=12"
nama_file = ambil_nama_file_dari_url(url)

if nama_file is not None:
    print(f"Nama file dari URL adalah: {nama_file}")
else:
    print("Tidak dapat menemukan nama file.")
