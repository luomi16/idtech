# The following program create an AI assistant that suggests restaurants.
from openai import OpenAI

client = OpenAI(
    api_key="your own api key that I gave you"
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

prompt = input("Enter a prompt: ")
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

print("\n############################################")
print("Thread id: " + thread.id)
print("Assistant id: " + ai_assistant.id)
print("############################################\n")

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=ai_assistant.id
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print("User: " + messages.data[1].content[0].text.value)
    print("Assistant: " + messages.data[0].content[0].text.value)

    print("\n############################################")
    print("Run id: " + run.id)
else:
    print(run.status)

# Please recommend a restaurant for Miya based on her preferences in the dataset. Include the name, cuisine, sub-city area, ratings, and suggested menu items including dessert.