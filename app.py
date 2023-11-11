from flask import Flask, render_template, request, jsonify
import openai
from openai import OpenAI
import time


app = Flask(__name__)

# Load the OPENAI_API_KEY from environment variable
openai.api_key = ''

# assistant = openai.beta.assistants.create(
#     model="gpt-4",
#     name="Math Tutor",
#     instructions="You are a personal math tutor. Write and run code to answer math questions.",
#     tools=[{"type": "code_interpreter"}]
# )
client = openai.OpenAI()

thread = client.beta.threads.create()


@app.route('/')
def index():
    return render_template('index.html')  # We will create this file next

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json['question']
    print(f"started")
    
   # add message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )

    print(f"{message.id}")

    # run assisstant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id='asst_bOwDS9uvj1LvbhfK1YFYecji',
    )
    
    # Poll the run status until it's complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        
        if run_status.status == 'completed':
            break
        time.sleep(0.5)  # Wait for 1 second before polling again
    
    
    messages =  client.beta.threads.messages.list(thread.id, order='desc')
    print(messages.data)

    print(messages.data[0].content[0].text.value)
   
    # print(messages.data[0].ThreadMessage.Text.value)

    response = messages.data[0].content[0].text.value

    # Assuming the response format includes the assistant's messages
    # and we are taking the last message sent by the assistant as the response.

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
    