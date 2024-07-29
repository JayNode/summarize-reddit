from openai import OpenAI
import summary
# link article from summary.py

def aimodel(article_body):

  client = OpenAI()

  assistant = client.beta.assistants.create(
    name="News Article Summarizer",
    instructions="_EMPTY_",
    model="gpt-3.5-turbo",
    tools=[{"type": "code_interpreter"}]
  )

  thread = client.beta.threads.create()

  # list of user games sent to content
  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=(article_body)
  )

  # instruction for finding most common genre from list of games
  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Summarize the text provided within 100 words"
  )

  while run.status != "completed":
      running = client.beta.threads.runs.retrieve(
          thread_id=thread.id,
          run_id=run.id
      )

      if running.status == "completed":
          break       

  all_messages = client.beta.threads.messages.list(
      thread_id=thread.id
  )

  print("----------------------------------------------------------------")
  # summarized article
  print(f"Summary: {message.content[0].text.value}")

  print("----------------------------------------------------------------")
  # results from chatgpt ai
  SUMM = all_messages.data[0].content[0].text.value
  print(f"VGRB: {SUMM}")

  return SUMM