from openai import AzureOpenAI
import re
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv('API_KEY'),
    api_version=os.getenv('API_VERSION'),
    azure_endpoint=os.getenv('AZURE_ENDPOINT')
)

def translate_content(post: str) -> tuple[bool, str]:
  try:
       # Check that post isn't empty
        if (not post or post.strip() == ''):
           return True, "The message is empty."
       
        # Check if post is gibberish
        gibberish_detection_context = "The following text given can be in any language. Identify if the following text is gibberish or malformed or incoherent for that language. Reply ONLY with 'Yes' or 'No'."
        gibberish_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": gibberish_detection_context},
                {"role": "user", "content": post}
            ]
        )
        
        gibberish_output = gibberish_response.choices[0].message.content.strip().lower()
        if gibberish_output not in ["yes", "no"]:
            raise ValueError("Unexpected format for gibberish detection response.")
        
        is_gibberish = gibberish_output == "yes"
        
        if is_gibberish:
            return True, "Unable to translate text because it is incoherent."
        
        # Check if the given content is in English or not
        language_detection_context = "Identify if the following text is in the English language. Reply ONLY with 'Yes' or 'No'."
        language_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": language_detection_context},
                {"role": "user", "content": post}
            ]
        )

        language_output = language_response.choices[0].message.content.strip().lower()
        if language_output not in ["yes", "no"]:
            raise ValueError("Unexpected format for language detection response.")

        is_english = language_output == "yes"

        if is_english:
            return (True, post)
        else:
            translation_context = "Translate the following text into English. Provide ONLY the translation, no explanations. Return the text with the style and punctuation it came in, do not change the punctuation. For example if I give you the text 'Esta es un mensaje en español', you should return 'This is a message in Spanish'. Do not return a period if the input didn't have one to begin with."
            translation_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": translation_context},
                    {"role": "user", "content": post}
                ]
            )

            translation = translation_response.choices[0].message.content.strip()
            if not translation:
                raise ValueError("Unexpected format for translation response.")

            return (False, translation)
  except Exception as e:
      print(f"error: {e}")
      return (False, "An error occurred while processing your request. Please try again later.")