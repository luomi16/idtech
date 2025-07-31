from flask import Flask, render_template, request, session
from openai import OpenAI

import os

app = Flask(__name__)
app.secret_key = "your_random_secret_key"  # Used for securely signing the session cookie

client = OpenAI(api_key="your_own_api_key")

# Global variables to store Assistant and File IDs after initialization
ASSISTANT_ID = None
FILE_ID = None

def init_openai():
    """
    Initialize the OpenAI Assistant and upload the dataset file if not already done.
    This is only run once per process for efficiency.
    """
    global ASSISTANT_ID, FILE_ID

    # Only initialize if IDs are not set yet
    if ASSISTANT_ID is None or FILE_ID is None:
        # Upload your restaurant dataset file
        with open("dataset.json", "rb") as f:
            data_file = client.files.create(file=f, purpose='assistants')
            FILE_ID = data_file.id

        # Create the specialized assistant with detailed instructions and tools
        assistant = client.beta.assistants.create(
            name="Restaurant Advisor",
            instructions=(
                "You are an application with special expertise in recommending restaurants based on the information "
                "you're provided with. Depending on the preferred cuisine, budget, and city, you are required to "
                "name a restaurant chain and suggest a few items from the menu, including dessert, for the person to "
                "try. You are also required to provide detailed information on the ratings, price range, "
                "and sub-city area."
            ),
            model="gpt-3.5-turbo",
            tools=[{"type": "file_search"}]
        )
        ASSISTANT_ID = assistant.id

@app.route("/", methods=["GET", "POST"])
def index():
    """
    The main chat route.
    Handles both GET (show chat UI) and POST (user submits a message).
    Keeps track of the chat history in the user session for a multi-turn experience.
    """
    # Ensure OpenAI assistant and file are initialized
    init_openai()

    # Initialize the session chat history if this is the first visit
    if "history" not in session:
        session["history"] = []

    result = None
    if request.method == "POST":
        # 1. Read the user's prompt from the submitted form
        user_msg = request.form["prompt"].strip()
        # 2. Add user's message to the chat history (role = "user")
        session["history"].append({"role": "user", "content": user_msg})
        session.modified = True  # Ensure session is saved

        # 3. Build the full chat history for OpenAI (user and assistant turns)
        messages = []
        for msg in session["history"]:
            if msg["role"] == "user":
                # Each user message needs to attach the dataset for file search
                messages.append({
                    "role": "user",
                    "content": msg["content"],
                    "attachments": [
                        {"file_id": FILE_ID, "tools": [{"type": "file_search"}]}
                    ]
                })
            else:
                # Assistant messages are plain content
                messages.append({
                    "role": "assistant",
                    "content": msg["content"]
                })

        # 4. Create a new OpenAI thread with the full conversation
        thread = client.beta.threads.create(messages=messages)

        # 5. Run the assistant on this thread and wait for completion
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # 6. If the run completed, fetch the assistant's reply
        if run.status == 'completed':
            all_msgs = client.beta.threads.messages.list(thread_id=thread.id)
            # The most recent message is from the assistant
            ai_msg = all_msgs.data[0].content[0].text.value
            # Add assistant reply to session history
            session["history"].append({"role": "assistant", "content": ai_msg})
            session.modified = True
            result = ai_msg  # For displaying the latest answer
        else:
            # If not complete, show the status for debugging
            result = f"Status: {run.status}"

    # Render the chat page with current chat history and latest reply (if any)
    return render_template(
        "index.html",
        prompt="",
        result=result,
        history=session.get("history", [])
    )

if __name__ == "__main__":
    # Run the Flask development server (debug=True for auto-reload)
    app.run(debug=True)
