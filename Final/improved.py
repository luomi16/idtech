# The following program create an AI assistant that suggests restaurants.
from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key="your_api_key_here",
)

open_file = open("dataset.json", "rb")

data_file = client.files.create(
    file=open_file,
    purpose='assistants'
)

ai_assistant = client.beta.assistants.create(
    name="Restaurant Advisor",
    instructions="You are an application with special expertise in recommending restaurants based on the information "
                 "you're provided with. Depending on the preferred cuisine, budget, and city, you are required to "
                 "name a restaurant chain and suggest a few items from the menu, including dessert, for the person to "
                 "try. You are also required to provide detailed information on the ratings, price range, "
                 "and sub-city area.",
    model="gpt-3.5-turbo",
    tools=[{"type": "file_search"}]
)

# while True:
#     prompt = input("Enter a prompt: ")
#
#     if prompt.lower() == 'exit':
#         print("Goodbye!")
#         break
#
#     thread = client.beta.threads.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt,
#                 "attachments": [
#                     {"file_id": data_file.id, "tools": [{"type": "file_search"}]}
#                 ]
#             }
#         ]
#     )
#
#     print("\n############################################")
#     print("Thread id: " + thread.id)
#     print("Assistant id: " + ai_assistant.id)
#     print("############################################\n")
#
#     run = client.beta.threads.runs.create_and_poll(
#         thread_id=thread.id,
#         assistant_id=ai_assistant.id
#     )
#
#     if run.status == 'completed':
#         messages = client.beta.threads.messages.list(
#             thread_id=thread.id
#         )
#         print("User: " + messages.data[1].content[0].text.value)
#         print("Assistant: " + messages.data[0].content[0].text.value)
#
#         print("\n############################################")
#         print("Run id: " + run.id)
#     else:
#         print(run.status)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    prompt = ""

    if request.method == "POST":
        prompt = request.form["prompt"]

        # Create thread and run
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "attachments": [
                        {"file_id": data_file.id, "tools": [{"type": "file_search"}]}
                    ]
                }
            ]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=ai_assistant.id
        )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            user_msg = messages.data[1].content[0].text.value
            assistant_msg = messages.data[0].content[0].text.value

            result = f"User: {user_msg}\n\nAssistant: {assistant_msg}"
        else:
            result = f"Run failed or not completed: {run.status}"

    return render_template("index.html", result=result, prompt=prompt)


if __name__ == "__main__":
    app.run(debug=True)


# Please recommend a restaurant for Miya based on her preferences in the dataset. Include the name, cuisine, sub-city area, ratings, and suggested menu items including dessert.