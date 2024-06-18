from openai import OpenAI
from window_focus import get_open_windows


class WindowClassifier:
    def __init__(self):
        self.api_key = "insert_your_api_key_here"
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = "gpt-3.5-turbo"

    def _get_response(self, messages, max_tokens=50):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name, messages=messages, max_tokens=max_tokens
            )
            if response.choices and hasattr(response.choices[0], "message"):
                decision_message = response.choices[0].message
                if hasattr(decision_message, "content"):
                    return decision_message.content.strip()
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_window_classification(self, title):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Classify this window title into a category: {title}",
            },
        ]
        return self._get_response(messages)

    def complete_text(self, goal):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Only return the user's message of the goal: {goal}",
            },
        ]
        return self._get_response(messages)

    @staticmethod
    def get_window_info(window_title):
        open_windows = get_open_windows()
        for window_info in open_windows:
            if window_title.lower() in window_info[0].lower():
                return window_info
        return None
