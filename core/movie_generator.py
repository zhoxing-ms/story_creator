import os
import json

from qwen_agent.utils.utils import print_traceback
from qwen_agent.llm.schema import Message
from core.agents import summary_story_agent
from core.text2image_icm import generate_image_from_text
from core.text2audio import generate_audio_from_text
from core.image2movie import generate_movie_from_resource_list


def generate_story_movie(messages):
    """处理生成完整故事按钮的点击事件"""
    try:
        # 先生成故事的8个步骤对应的摘要
        if not messages:
            return "暂无故事素材", None
        messages.append(Message('user', '请生成以上完整故事的6-8个步骤的中英文摘要信息吧'))
        summary_response = summary_story_agent.run_nonstream(messages)
        if not summary_response or not summary_response[0] or not summary_response[0]['content']:
            return "故事生成失败！", None
        story_summary = summary_response[0]['content']
        step_desc_list = json.loads(story_summary)
        # 分别生成每个故事步骤对应的图片和音频

        audio_list = []
        image_list = []
        text_list = []
        for step_desc in step_desc_list:
            step_parts = step_desc.split("|")

            chinese_desc = step_parts[0]
            text_list.append(chinese_desc)

            audio_path = generate_audio_from_text(chinese_desc)
            audio_list.append(audio_path)

            english_desc = step_parts[1]
            image_path = generate_image_from_text(english_desc)
            image_list.append(image_path)

        # 用图片和音频素材生成电影
        movie_path = generate_movie_from_resource_list(image_list, audio_list, text_list)
        if movie_path:
            return "故事生成成功！", movie_path
        return "故事生成成功，但未找到视频文件", None
    except Exception as e:
        print_traceback()
        return f"生成失败：{str(e)}", None


if __name__ == '__main__':
    messages=[
        {"role": "user", "content": "请讲一个森林里小动物的故事"},
        {"role": "assistant", "content": "在遥远的森林里，有一只勇敢的小兔子，名叫莉莉。有一天，她在森林深处发现了一扇闪着金光的大门。她决定探索这扇门背后的秘密。当莉莉触摸大门时，大门缓缓开启，她被一道光芒包围，醒来发现自己来到了一个充满未知的世界，这个世界充满了各种奇异的生物和景象。在这个世界里，莉莉遇到了各种各样的新朋友，包括会说话的树木、能够飞翔的蘑菇、以及能变色的石头。每一种生物都拥有一种特殊的能力，它们帮助莉莉解开这里的谜团，探索这个世界的奥秘。有一天，莉莉发现了一个巨大的水晶球，它散发出温暖的光芒，似乎在引导她寻找某种重要的物品。在朋友们的帮助下，莉莉找到了这个物品——一颗闪耀着七彩光芒的宝石。据说这颗宝石拥有改变世界的力量。在朋友们的支持下，莉莉小心翼翼地将宝石放置回水晶球中，刹那间，整个世界都被一阵耀眼的光芒所覆盖。光芒渐渐消散后，莉莉惊讶地发现，这个世界变得更加和谐美丽，每一种生物都和平共处，相互帮助。莉莉和她的朋友们在这个充满奇迹的世界里生活得非常开心。他们一起解决了许多难题，让这个世界变得更加美好。随着时间的流逝，莉莉学会了更多的知识和技能，她成为了这个世界的守护者，保护着这个世界永远充满光明和希望。"},
    ]
    generate_story_movie(messages)
