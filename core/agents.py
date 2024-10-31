"""Customize an agent to implement visual storytelling"""
import json5
import openvino.properties as props
import openvino.properties.hint as hints
import openvino.properties.streams as streams

from pathlib import Path
from modelscope import snapshot_download

from core.prompt import story_telling_prompt, painting_prompt, summary_story_prompt
from core.text2image_icm import generate_image_from_text
from core.text2audio import generate_audio_from_text
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.agents import Assistant
from qwen_agent.agents import Assistant
from qwen_agent.tools import BaseTool


llm_model_id = "snake7gun/Qwen2-7B-Instruct-int4-ov"
llm_local_path  = "model/snake7gun/Qwen2-7B-Instruct-int4-ov"

if not Path(llm_local_path).exists():
    model_dir = snapshot_download(llm_model_id, cache_dir="./model/")

@register_tool("image_generation")
class ImageGeneration(BaseTool):
    description = "AI绘画(图像生成)工具，输入所需要图片内容的文本描述，并返回基于文本信息绘制生成的图像的本地保存路径。"
    parameters = [{"name": "image_desc", "type": "string", "description": "所需图像内容的精简描述，请注意描述内容必须使用英语，而且英文描述不能超过10个单词", "required": True}]

    def call(self, params: str, **kwargs) -> str:
        image_desc = json5.loads(params)["image_desc"]
        return generate_image_from_text(image_desc)

@register_tool("audio_generation")
class AudioGeneration(BaseTool):
    description = "音频生成工具，根据输入的文本内容生成对应的音频并返回音频的本地保存路径。"
    parameters = [{"name": "audio_desc", "type": "string", "description": "需要生成对应音频的文本内容", "required": True}]

    def call(self, params: str, **kwargs) -> str:
        audio_desc = json5.loads(params)["audio_desc"]
        return generate_audio_from_text(audio_desc)

ov_config = {
    hints.performance_mode(): hints.PerformanceMode.LATENCY, 
    streams.num(): "1", 
    props.cache_dir(): ""
}

llm_cfg = {
    "ov_model_dir": llm_local_path,
    "model_type": "openvino",
    "device": "GPU",
    "ov_config": ov_config,
    # (Optional) LLM hyperparameters for generation:
    "generate_cfg": {
        "top_p": 0.8,
        "max_new_tokens": 1000
    },
}

story_telling_agent = Assistant(llm=llm_cfg, 
                                function_list=["audio_generation"],
                                system_message=story_telling_prompt,
                                files=['resource/如何讲童话故事.txt'],
                                name = 'story_telling_agent')

painting_agent = Assistant(llm=llm_cfg, 
                           function_list=["image_generation"],
                           system_message=painting_prompt,
                           name = 'painting_agent')

summary_story_agent = Assistant(llm=llm_cfg, 
                                system_message=summary_story_prompt,
                                name = 'summary_story_agent')
