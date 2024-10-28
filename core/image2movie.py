import random
import datetime

from moviepy.editor import *

"""
定义Scene类，对应每一幕，使用图片路径、音频路径、文本字符串创建一个Scene对象。
调用generate_movie_from_scenes生成视频，参数为Scene列表。
"""


class Scene:
    def __init__(self, image_file, audio_file, text):
        self.image_file = image_file
        self.audio_file = audio_file
        self.text = text


def generate_movie_from_scenes(scenes):

    # 视频剪辑列表
    video_clips = []

    for scene in scenes:
        audio_clip = AudioFileClip(scene.audio_file)
        duration = audio_clip.duration  # 将图片时长设置为音频的时长

        # 读取图片，创建视频剪辑
        image_clip = ImageClip(scene.image_file, duration=duration)

        # 为视频剪辑添加音频
        image_with_caption = image_clip.set_audio(audio_clip)

        # 添加到视频剪辑列表
        video_clips.append(image_with_caption)

    # 合并所有剪辑
    final_video = concatenate_videoclips(video_clips, method="compose")

    # 导出视频
    random_movie_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1,10)) for i in range(5)])
    movie_path = os.path.join("temp", "image", random_movie_name + ".mp4")
    final_video.write_videofile(movie_path, codec="libx264", fps=24)


def generate_movie_from_materials(image_list, vedio_list, text_list):
    if image_list.length != vedio_list.length or vedio_list.length != text_list.length:
        return ""

    sceneList = []
    for image, vedio, text in zip(image_list, vedio_list, text_list):
        scene = Scene(image, vedio, text)
        sceneList.append(scene)

    # 定义图片、文字和音频文件
    generate_movie_from_scenes(sceneList)
