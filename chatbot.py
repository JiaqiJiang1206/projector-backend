# from openai import OpenAI
# from config import apiKey

# class ChatBot:
#   def __init__(self, systemPrompt, model: str = "gpt-4o-2024-11-20") -> None:
#     self.client = OpenAI(
#         api_key=apiKey,
#         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#     )
#     self.model = model
#     self.conversation_history = [
#       {'role': 'system', 'content': systemPrompt}
#     ]
  
#   def add_user_message(self, content: str):
#     """Add a user message to the conversation history."""
#     self.conversation_history.append({'role': 'user', 'content': content})
  
#   def get_reply(self) -> str:
#     """Call the model and get a reply."""
#     completion = self.client.chat.completions.create(
#         model=self.model,
#         messages=self.conversation_history,
#     )
#     assistant_output = completion.choices[0].message.content
#     self.conversation_history.append({'role': 'assistant', 'content': assistant_output})
#     return assistant_output
  
from openai import OpenAI
client = OpenAI()

my_assistant = client.beta.assistants.retrieve("asst_abc123")
print(my_assistant)


message_thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Hello, what is AI?"
    },
    {
      "role": "user",
      "content": "How does AI work? Explain it in simple terms."
    },
  ]
)

print(message_thread)

thread_message = client.beta.threads.messages.create(
  "thread_abc123",
  role="user",
  content="How does AI work? Explain it in simple terms.",
)
