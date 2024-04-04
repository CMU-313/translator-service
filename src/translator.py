# import google.generativeai as genai
# import os
# from google.colab import userdata  #Used to securely store API Key

import bigframes.dataframe
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from google.cloud import aiplatform
from google.auth.credentials import Credentials
from google.oauth2 import service_account

PROJECT_ID = "nodebb-417218"

credentials, project = google.auth.default()

# credentials = Credentials.from_service_account_info({
#     "type": "service_account",
#     "project_id": PROJECT_ID
#     "private_key_id": 
#     "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR-PRIVATE-KEY\n-----END PRIVATE KEY-----\n",
#     "client_email": 
#     "client_id": 
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": 
# })

aiplatform.init(
  # your Google Cloud Project ID or number
  # environment default used is not set
  project=PROJECT_ID,

  # credentials
  credentials=credentials,
)

GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)

# LLM Settings
chat_model = ChatModel.from_pretrained("chat-bison@001")

get_translation_context = ("Forget everything from before."
           " I am an avid linguist that loves learning about languages and different cultures, however I only know English."
           " You will now be my expert translator and who can translate text from any language into English.")

def get_translation(post: str) -> str:
  # ----------------- DO NOT MODIFY ------------------ #

  parameters = {
      "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
      "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
  }

  # ---------------- YOUR CODE HERE ---------------- #
  chat = chat_model.start_chat(context=context1)
  response = chat.send_message(post, **parameters)
  return response.text

get_language_context = ("Forget everything from before."
           " I am an avid linguist that loves learning about languages and different cultures, however can easily get"
           " confused between English and non-English words. Sometimes I also become confused with whether some English"
           " dialects are actually English or not. You will now be my expert translator and who can correctly tell"
           " me what language the text is. Give your answer in one word.")

def get_language(post: str) -> str:
  # ----------------- DO NOT MODIFY ------------------ #

  parameters = {
      "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
      "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
  }

  # ---------------- YOUR CODE HERE ---------------- #
  chat = chat_model.start_chat(context=context2)
  response = chat.send_message(post, **parameters)
  return response.text

# If the input text is in English, then return (True, input_text). If the input text is not in english, but is in a known language, return 
# (False, translation of input text). If it is not able to indentify the language or the translation return (True, error)
def query_llm_robust(post: str) -> tuple[bool, str]:
#   parameters = {
#     "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
#     "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
#   }
#   chat = chat_model.start_chat(context=context3)
#   response = chat.send_message(post, **parameters)
  eror_result = (True, '<LangError>: Post text LLM response is malformed')

  langauge = get_language(post)
  if type(language) != str or language != '':
    # Failed to get language
    return error_result

  language = language.lower()
  
  translation = get_translation(post)
  if type(translation) != str:
    # Failed to get translation
    return error_result
  
  print(f"Language: {language}, Translation: {translation}")

  lang_check = langauge == 'english'
  return (lang_check, translation)

def translate_content(content: str) -> tuple[bool, str]:
    return query_llm_robust(post)