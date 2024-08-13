import os
from openai import OpenAI

import chunking

# link article from summary.py

def aimodel(article_body):

  client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
  )

  # input_chunks = chunking.split_text(article_body)
  output_chunks = []

  print("Entered gpt")
  count = 0

  for chunk in article_body:

    print("count: " , count)
    count+=1

    response = client.completions.create(
      model="gpt-4o-mini",
      prompt=(f"You are a creative and experienced copywriter. Please write a unique summary of the following text using friendly, easy to read language:\n{chunk}\n\nSummary:"),
      temperature=0.5,
      max_tokens=1024,
      n = 1,
      stop=None
    )

  summary = response.choices[0].text.strip()
  output_chunks.append(summary)

  return " ".join(output_chunks)

  # assistant = client.beta.assistants.create(
  #   name="News Article Summarizer",
  #   instructions="_EMPTY_",
  #   model="gpt-3.5-turbo",
  #   tools=[{"type": "code_interpreter"}]
  # )

  # thread = client.beta.threads.create()

  # list of user games sent to content
  # message = client.beta.threads.messages.create(
  #     thread_id=thread.id,
  #     role="user",
  #     content=(article_body)
  # )

  # print("gpt - article")

  # instruction for finding most common genre from list of games
  # run = client.beta.threads.runs.create(
  #   thread_id=thread.id,
  #   assistant_id=assistant.id,
  #   instructions="You are a creative and experienced copywriter. Please write a unique summary of the following text using friendly, easy to read language:"
  # )


  # count = 0
  # while run.status != "completed":
  #     print("count:" , count)
  #     count+=1
  #     running = client.beta.threads.runs.retrieve(
  #         thread_id=thread.id,
  #         run_id=run.id
  #     )

  #     if running.status == "completed":
  #         break       

  # all_messages = client.beta.threads.messages.list(
  #     thread_id=thread.id
  # )

  # print("----------------------------------------------------------------")
  # # summarized article
  # print(f"Summary: {message.content[0].text.value}")

  # print("----------------------------------------------------------------")
  # # results from chatgpt ai
  # SUMM = all_messages.data[0].content[0].text.value
  # print(f"Article: {SUMM}")

  # return SUMM
