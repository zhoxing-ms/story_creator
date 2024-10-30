from ui.website_ui import WebUI
# from core.story_telling import story_telling_bot

chatbot_config = {
    'prompt.suggestions': [
        '请讲个安徒生童话',
        '请讲个白雪公主的故事',
        '请以齐天大圣的西天取经路为原型编一个新故事',
    ],
    'agent.avatar': "resource/avatar.png"
}

# 初始化WebUI实例时传入这个DummyAgent
class DummyAgent:
    def __init__(self):
        self.name = "Placeholder Agent"
        self.description = "This is a dummy agent for UI preview."
        self.function_map = None


if __name__ == '__main__':
    WebUI(
        agent=DummyAgent(),
        chatbot_config=chatbot_config,
    ).run()
