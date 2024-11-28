import random
import datetime
import os
import json

from moviepy.editor import *

"""
定义Scene类，对应每一幕，使用图片路径、音频路径、文本字符串创建一个Scene对象。
调用generate_movie_from_scenes生成视频，参数为Scene列表。
"""


class Scene:
    def __init__(self, image_file, audio_file):
        self.image_file = image_file
        self.audio_file = audio_file


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
    movie_path = os.path.join("temp", "movie", random_movie_name + ".mp4")
    final_video.write_videofile(movie_path, codec="libx264", fps=24)


def get_files_list():
    """
    读取audio和image文件夹中的内容
    返回两个列表：audio_list 和 image_list
    """

    # 初始化结果列表
    audio_list = []
    image_list = []
    
    # 读取audio文件夹
    audio_path = 'temp/audio'
    if os.path.exists(audio_path):
        for file in os.listdir(audio_path):
            file_path = os.path.join(audio_path, file)
            audio_list.append(file_path)


    # 读取image文件夹
    image_path = 'temp/image'
    if os.path.exists(image_path):
        for file in os.listdir(image_path):
            file_path = os.path.join(image_path, file)
            image_list.append(file_path)
    
    return  image_list, audio_list


def generate_movie_from_lists(image_list, audio_list):
    """
    从图片列表和音频列表生成视频
    Args:
        image_list: 图片文件路径列表
        audio_list: 音频文件路径列表
    Returns:
        str: 生成的视频路径，如果失败则返回空字符串
    """
    if len(image_list) != len(audio_list):
        return ""

    scene_list = []
    for image_path, audio_path in zip(image_list, audio_list):
        if not os.path.exists(image_path) or not os.path.exists(audio_path):
            print("File not found:", image_path if not os.path.exists(image_path) else audio_path)
            continue
        scene = Scene(image_path, audio_path)
        scene_list.append(scene)

    generate_movie_from_scenes(scene_list)

def generate_movie_from_materials():
    """
    获取image_list, audio_list，生成视频
    """
    image_list, audio_list = get_files_list()

    return generate_movie_from_lists(image_list, audio_list)
