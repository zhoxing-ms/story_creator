from ui.website_ui import WebUI
from core.story_telling import story_telling_bot

chatbot_config = {
    'prompt.suggestions': [
        '请讲个安徒生童话',
        '请讲个白雪公主的故事',
        '请以齐天大圣的西天取经路为原型编一个新故事',
    ],
    'agent.avatar': "resource/avatar.png"
}

if __name__ == '__main__':
    WebUI(
        story_telling_bot,
        chatbot_config=chatbot_config,
    ).run()
