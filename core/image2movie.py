import random
import datetime
import os
from pypinyin import pinyin, Style
from moviepy.editor import AudioFileClip, ImageClip, TextClip, concatenate_videoclips, CompositeVideoClip

# os.environ['IMAGEIO_FFMPEG_EXE'] = 'ffmpeg'

"""
定义Scene类，对应每一幕，使用图片路径、音频路径、文本字符串创建一个Scene对象。
调用generate_movie_from_scenes生成视频，参数为Scene列表。
"""

withPinYin = True


class Scene:
    def __init__(self, image_file, audio_file, text):
        self.image_file = image_file
        self.audio_file = audio_file
        self.text = text
        self.pinyin_text = self.generate_pinyin(text) if withPinYin == True else " "

    # 将中文文本转换为拼音
    def generate_pinyin(self, text):
        pinyin_text = ' '.join([' '.join(item) for item in pinyin(text, style=Style.TONE)])
        return pinyin_text

def generate_movie_from_scenes(scenes):
    video_clips = []

    for scene in scenes:
        audio_clip = AudioFileClip(scene.audio_file)
        duration = audio_clip.duration

        image_clip = ImageClip(scene.image_file)
        image_clip.duration = duration

        # 创建字幕剪辑
        text_clip = TextClip(scene.text, font='resource/FZSTK.TTF', fontsize=24, color="white")
        text_clip = text_clip.set_position(("center", "center"))
        text_clip.duration = duration

        pinyin_clip = TextClip(scene.pinyin_text, font='resource/FZSTK.TTF', fontsize=23, color="white")
        pinyin_clip = pinyin_clip.set_position(("center", 0.51), True) 
        pinyin_clip.duration = duration

        vedio_clip = CompositeVideoClip([image_clip, text_clip, pinyin_clip]).set_audio(audio_clip)
        vedio_clip.duration = duration

        video_clips.append(vedio_clip)

    final_video = concatenate_videoclips(video_clips, method="compose")

    random_movie_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1, 10)) for _ in range(5)])
    movie_path = os.path.join("temp", "movie", random_movie_name + ".mp4")
    final_video.write_videofile(movie_path, codec="libx264", fps=24)
    return movie_path

def generate_movie_from_resource_list(image_list, audio_list, text_list):
    """
    从图片列表和音频列表生成视频
    Args:
        image_list: 图片文件路径列表
        audio_list: 音频文件路径列表
    Returns:
        str: 生成的视频路径，如果失败则返回空字符串
    """
    if len(image_list) != len(audio_list) or len(audio_list) != len(text_list):
        return ""

    scene_list = []
    for image_path, audio_path, text in zip(image_list, audio_list, text_list):
        if not os.path.exists(image_path) or not os.path.exists(audio_path):
            print("File not found:", image_path if not os.path.exists(image_path) else audio_path)
            continue
        scene = Scene(image_path, audio_path, text)
        scene_list.append(scene)

    return generate_movie_from_scenes(scene_list)

if __name__ == '__main__':
    image_list = ["temp/image/2024103119464248885723965.jpg", "temp/image/2024103119464870756483389.jpg"]
    audio_list = ["temp/audio/2024103119464248686089455.mp3", "temp/audio/2024103119465599362594685.mp3"]
    text_list = ["小兔子丽丽的故事", "大兔子宝宝的故事"]
    generate_movie_from_resource_list(image_list, audio_list, text_list)
