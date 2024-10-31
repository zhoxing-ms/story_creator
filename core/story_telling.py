import copy

from typing import Dict, Iterator, List, Optional, Union
from qwen_agent.llm import BaseChatModel
from qwen_agent.llm.schema import Message
from qwen_agent import Agent
from core.agents import story_telling_agent, painting_agent
from qwen_agent.tools import BaseTool


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

        new_messages.append(Message('user', '请根据以上故事内容的场景生成一组图片吧!'))
        for rsp in self.painting_agent.run(new_messages, lang=lang, **kwargs):
            yield response + rsp

story_telling_bot = VisualStorytelling()
