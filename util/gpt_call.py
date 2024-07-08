from functools import cached_property
import os
from dotenv import load_dotenv
import openai
from retry import retry
from openai import OpenAI


class OpenAIClient:

    SINGLETON_CLIENT = None
    SINGLETON_OPENAI = None

    @cached_property
    def is_openai_enabled(self):
        print("Checking for OpenAI API key...")
        load_dotenv()
        if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
            # Print warning message in red.
            print(
                "\033[91m"
                + "WARNING: OpenAI API key not found. OpenAI will not be used."
                + "\033[0m"
            )
            return False
        else:
            return True

    @retry(tries=3, delay=3.0)
    def get_completion(self, prompt: str, max_tokens: int = 128, n: int = 1):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = OpenAIClient.SINGLETON_OPENAI.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=n
        )
        print(response.choices[0].message)
        return response


def gpt_client():
    if OpenAIClient.SINGLETON_CLIENT is None:
        OpenAIClient.SINGLETON_CLIENT = OpenAIClient()
        OpenAIClient.SINGLETON_OPENAI = OpenAI()
    return OpenAIClient.SINGLETON_CLIENT
