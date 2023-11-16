from qrLogin import qr_login
from getDynamicReposts import fetch_latest_updates
from getLastestVedios import get_latest_videos
from vedio import download_video_and_audio
from get_bvid_cid import get_bvid_from_url, get_cid
import re

# 设置您的cookie信息
cookie = '0013f548%2C1715380651%2C87702%2Ab2CjAYU9lFGbG9MnsN9gf9C-7hkQog0uV96AOZcBpeDxqqvNegEN2hnQ6EuQqvBjjFI64SVmVXTGw3X29kUXVuQ1NJQ0NQVUpXbko1N2FVN2luSkJnZjRMaFNabWJpNzNXdnlSQXZ1X1ZnekZKTzZzLTdlbTRud1I5SkFIMWZ4aXJNY3BYNWRieFBBIIEC'

# 设置视频和音频的基本存储路径
base_video_path = '/Volumes/Seagate Hub/Youtube/Raw file/'
base_audio_path = '/Volumes/Seagate Hub/Youtube/Raw file/'
base_merged_output_path = '/Volumes/Seagate Hub/Youtube/final/'


session = qr_login()
if session:
    data = fetch_latest_updates(session)
    if data and data['code'] == 0:
        up_list = data['data']['up_list']
        for up in up_list:
            if up['has_update']:
                latest_video = get_latest_videos(up['mid'], session)
                if latest_video:
                    video_title = latest_video['title']
                    # 清理文件名中的非法字符
                    clean_title = re.sub(r'[\\/*?:"<>|]', '_', video_title)
                    video_save_path = f"{base_video_path}{clean_title}.mp4"
                    audio_save_path = f"{base_audio_path}{clean_title}.mp4"
                    merged_output_path = f"{base_merged_output_path}{clean_title}.mp4"

                    video_url = f"https://www.bilibili.com/video/{latest_video['bvid']}"
                    bvid = get_bvid_from_url(video_url)
                    if bvid:
                        cid = get_cid(bvid)
                        if cid:
                            download_video_and_audio(bvid, cid, cookie, video_save_path, audio_save_path, merged_output_path)
else:
    print("登录失败")