"""Customize an agent to implement visual storytelling"""
import copy

import json5
import openvino.properties as props
import openvino.properties.hint as hints
import openvino.properties.streams as streams

from typing import Dict, Iterator, List, Optional, Union
from core.prompt import story_telling_prompt, painting_prompt
from core.text2image import generate_image_from_text
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.agents import Assistant
from qwen_agent import Agent
from qwen_agent.agents import Assistant
from qwen_agent.llm import BaseChatModel
from qwen_agent.llm.schema import ContentItem, Message
from qwen_agent.tools import BaseTool


llm_model_id = "Qwen/Qwen2-7B-Instruct"
llm_local_path  = "model/snake7gun/Qwen2-7B-Instruct-int4-ov"


@register_tool("image_generation")
class ImageGeneration(BaseTool):
    description = "AI绘画(图像生成)工具，输入所需要图片内容的文本描述，并返回基于文本信息绘制生成的图像的本地路径。"
    parameters = [{"name": "image_desc", "type": "string", "description": "所需图像内容的精简描述，请注意描述内容必须使用英语，而且英文描述不能超过10个单词", "required": True}]

    def call(self, params: str, **kwargs) -> str:
        image_desc = json5.loads(params)["image_desc"]
        return generate_image_from_text(image_desc)

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
        "max_new_tokens": 800
    },
}

story_telling_agent = Assistant(llm=llm_cfg, 
                                system_message=story_telling_prompt,
                                files=['resource/如何讲童话故事.txt'],
                                name = 'story_telling_agent')

painting_agent = Assistant(llm=llm_cfg, 
                           function_list=["image_generation", "code_interpreter"],
                           system_message=painting_prompt,
                           name = 'painting_agent')

class VisualStorytelling(Agent):
    """Customize an agent for writing story from pictures"""

    def __init__(self,
                 function_list: Optional[List[Union[str, Dict, BaseTool]]] = None,
                 llm: Optional[Union[Dict, BaseChatModel]] = None):
        super().__init__(llm=llm)

        self.story_telling_agent = story_telling_agent

        self.painting_agent = painting_agent

        self.name = '故事造梦者'

        self.description = "和我一起创造有趣生动的梦幻故事吧!"

    def _run(self, messages: List[Message], lang: str = 'zh', **kwargs) -> Iterator[List[Message]]:
        """Define the workflow"""

        assert isinstance(messages[-1]['content'], list)

        new_messages = copy.deepcopy(messages)
        # new_messages[-1]['content'].append(ContentItem(text='请描述这个故事的一部分，并给出后续可能发展的3个选项和1个自由发挥选项'))
        response = []
        for rsp in self.story_telling_agent.run(new_messages):
            yield response + rsp
        response.extend(rsp)
        new_messages.extend(rsp)

        new_messages.append(Message('user', '请根据以上故事内容的场景(忽略上面内容的4个选项)生成一张图片吧!'))
        for rsp in self.painting_agent.run(new_messages, lang=lang, **kwargs):
            yield response + rsp


story_telling_bot = VisualStorytelling()
