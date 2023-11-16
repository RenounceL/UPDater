import subprocess

import requests
import re
from tqdm import tqdm
import concurrent.futures

# 下载媒体（视频或音频）的函数
def download_media(url, headers, save_path, media_type="Media", position=0):
    with requests.get(url, headers=headers, stream=True) as r:
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=f"Downloading {media_type}", position=position, colour='green')
        with open(save_path, 'wb') as file:
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

# 下载视频和音频的函数
def download_video_and_audio(bvid, cid, cookie, video_save_path, audio_save_path, merged_output_path):
    url = f'https://api.bilibili.com/x/player/playurl?fnval=16&cid={cid}&bvid={bvid}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': f'https://www.bilibili.com/video/{bvid}',
        'Cookie': f'SESSDATA={cookie}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        video_url = data['data']['dash']['video'][0]['baseUrl']
        audio_url = data['data']['dash']['audio'][0]['baseUrl']

        # 使用多线程同时下载视频和音频
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_video = executor.submit(download_media, video_url, headers, video_save_path, "Video", 0)
            future_audio = executor.submit(download_media, audio_url, headers, audio_save_path, "Audio", 1)

        future_video.result()
        future_audio.result()

        print(f"视频和音频下载完成，已保存至 {video_save_path} 和 {audio_save_path}")
        merge_video_and_audio(video_save_path, audio_save_path, merged_output_path)
        print(f"合并完成，文件保存为 {merged_output_path}")
    else:
        print("下载视频和音频错误：", response.status_code)


def merge_video_and_audio(video_path, audio_path, output_path):
    cmd = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_path]
    subprocess.run(cmd)

