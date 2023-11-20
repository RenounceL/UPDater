import subprocess
import requests
from tqdm import tqdm
import multiprocessing
from multiprocessing import Manager
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, filename='Doc/UPdater.log', format='%(asctime)s - %(levelname)s - %(message)s')


# def download_media(url, headers, save_path, media_type="Media", position=0, lock=None):
#     logging.info(f"Starting download for {media_type}: {url}")
#     total_size_in_bytes = int(requests.head(url, headers=headers).headers.get('content-length', 0))
#     block_size = 1024 * 1024  # 1 Mebibyte
#
#     with lock:
#         progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=f"Downloading {media_type}",
#                             position=position, leave=False)
#
#     with requests.get(url, headers=headers, stream=True) as r:
#         with open(save_path, 'wb') as file:
#             for data in r.iter_content(block_size):
#                 with lock:
#                     progress_bar.update(len(data))
#                 file.write(data)
#         progress_bar.close()
#
#     logging.info(f"Download completed for {media_type}: {url}")
#
#
# def download_video_and_audio(bvid, cid, cookie, video_save_path, audio_save_path, merged_output_path):
#     url = f'https://api.bilibili.com/x/player/playurl?fnval=16&cid={cid}&bvid={bvid}'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#         'Referer': f'https://www.bilibili.com/video/{bvid}',
#         'Cookie': f'SESSDATA={cookie}'
#     }
#     response = requests.get(url, headers=headers)
#
#     if response.status_code == 200:
#         data = response.json()
#         video_url = data['data']['dash']['video'][0]['baseUrl']
#         audio_url = data['data']['dash']['audio'][0]['baseUrl']
#
#         # 使用 multiprocessing 来同时下载视频和音频
#         manager = Manager()
#         lock = manager.Lock()
#         processes = []
#
#         video_process = multiprocessing.Process(target=download_media,
#                                                 args=(video_url, headers, video_save_path, "Video", 0, lock))
#         audio_process = multiprocessing.Process(target=download_media,
#                                                 args=(audio_url, headers, audio_save_path, "Audio", 1, lock))
#
#         video_process.start()
#         audio_process.start()
#         processes.append(video_process)
#         processes.append(audio_process)
#
#         for process in processes:
#             process.join()
#
#         # 合并视频和音频
#         merge_video_and_audio(video_save_path, audio_save_path, merged_output_path)
#     else:
#         print("下载视频和音频错误：", response.status_code)


def download_with_aria2(url, save_path, headers):
    save_path = Path(save_path)
    header_args = ' '.join([f'--header="{k}: {v}"' for k, v in headers.items()])
    command = f"aria2c --auto-file-renaming=false --download-result=hide --allow-overwrite=true --console-log-level=warn -x16 -s16 -j16 -k5M {header_args} \"{url}\" -d \"{save_path.parent}\" -o \"{save_path.name}\""
    subprocess.run(command, shell=True)

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

        # 使用 multiprocessing 来同时下载视频和音频
        manager = Manager()
        processes = []

        video_process = multiprocessing.Process(target=download_with_aria2,
                                                args=(video_url, video_save_path, headers))
        audio_process = multiprocessing.Process(target=download_with_aria2,
                                                args=(audio_url, audio_save_path, headers))

        video_process.start()
        audio_process.start()
        processes.append(video_process)
        processes.append(audio_process)

        for process in processes:
            process.join()

        # 合并视频和音频
        merge_video_and_audio(video_save_path, audio_save_path, merged_output_path)
    else:
        print("下载视频和音频错误：", response.status_code)

def merge_video_and_audio(video_path, audio_path, output_path):
    cmd = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
           output_path]
    subprocess.run(cmd)
