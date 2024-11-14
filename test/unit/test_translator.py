from src.translator import translate_content
from typing import Tuple

def test_llm_normal_response():
    test_cases = [
        ("Hello, how are you?", (True, "how are you")),
        ("Bonjour tout le monde", (False, "Hello everyone")),
        ("Das ist ein test", (False, "test")),
        ("This is an English message", (True, "English")),
        ("这是一条中文消息", (False, "Chinese")),
        ("Ceci est un message en français", (False, "French")),
        ("Esta es un mensaje en español", (False, "Spanish")),
        ("Esta é uma mensagem em português", (False, "Portuguese")),
        ("これは日本語のメッセージです", (False, "Japanese")),
        ("이것은 한국어 메시지입니다", (False, "Korean")),
        ("Dies ist eine Nachricht auf Deutsch", (False, "German")),
        ("Questo è un messaggio in italiano", (False, "Italian")),
        ("Это собщение на русском", (False, "Russian")),
        ("هذه رسالة باللغة العربية", (False, "Arabic")),
        ("यह हिंदी में संदेश है", (False, "Hindi")),
        ("นี่คือข้อความภาษาไทย", (False, "Thai")),
        ("Bu bir Türkçe mesajdır", (False, "Turkish")),
        ("Đây là một tin nhắn bằng tiếng Việt", (False, "Vietnamese")),
        ("Esto es un mensaje en catalán", (False, "Catalan")),
    ]
    for input_text, expected in test_cases:
        is_english, translated = translate_content(input_text)
        assert is_english == expected[0], f"Expected is_english={expected[0]} but got {is_english}"
        assert expected[1] in translated, f"Expected translation to contain '{expected[1]}' but got '{translated}'"

def test_llm_gibberish_response():
    test_cases = [
        ("asdfasldkfja", (True, "Unable to translate text because it is incoherent.")),
        ("!@#$%^&*()", (True, "Unable to translate text because it is incoherent.")),
        ("我工程夠外邊後珍珠奶茶", (True, "Unable to translate text because it is incoherent.")),
        ("", (True, "The message is empty.")),
        ("   ", (True, "The message is empty.")),
    ]
    for input_text, expected in test_cases:
        is_english, translated = translate_content(input_text)
        assert is_english == expected[0], f"Expected is_english={expected[0]} but got {is_english}"
        assert expected[1] in translated, f"Expected translation to contain '{expected[1]}' but got '{translated}'"