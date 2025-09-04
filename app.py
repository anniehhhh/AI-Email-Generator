from flask import Flask, request, jsonify
from langchain_groq import ChatGroq
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Allow frontend on different port to access this backend

import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

@app.route('/')
def home():
    return "AI Email Generator Backend is Running!"

@app.route('/generate-reply', methods=['POST'])
# def generate_reply():
#     data = request.get_json()
#     received_email = data.get('received_email', '')
#     tone = data.get('tone', 'neutral').lower()

#     if not received_email:
#         return jsonify({"error": "No received email provided"}), 400

#     prompt = (
#         f"You are an AI assistant. Craft a professional and concise reply to the following email. "
#         f"Make the tone {tone}.\n\nEmail:\n{received_email}\n\nReply:"
#     )

#     try:
#         response = llm.invoke(prompt)
#         return jsonify({"reply": response})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
@app.route('/generate-reply', methods=['POST'])
def generate_reply():
    data = request.get_json()
    received_email = data.get('received_email', '')
    tone = data.get('tone', 'neutral').lower()
    generate_multiple = data.get('generate_multiple', False)

    if not received_email:
        return jsonify({"error": "No received email provided"}), 400

    if generate_multiple:
        # Generate three different replies with different tones
        tones = ["formal", "concise", "creative"]
        replies = []

        for current_tone in tones:
            prompt = (
                f"You are an AI assistant. Craft a professional reply to the following email. "
                f"Make the tone {current_tone}.\n\nEmail:\n{received_email}\n\nReply:"
            )
            try:
                response = llm.invoke(prompt)
                reply_text = response.content
                replies.append({"tone": current_tone, "reply": reply_text})
            except Exception as e:
                print(f"Error generating {current_tone} reply:", e)
                replies.append({"tone": current_tone, "reply": f"Error generating {current_tone} reply: {str(e)}"})

        return jsonify({"replies": replies})
    else:
        # Generate a single reply with the specified tone
        prompt = (
            f"You are an AI assistant. Craft a professional and concise reply to the following email. "
            f"Make the tone {tone}.\n\nEmail:\n{received_email}\n\nReply:"
        )

        try:
            response = llm.invoke(prompt)
            reply_text = response.content  # Extract the actual string reply
            return jsonify({"reply": reply_text})

        except Exception as e:
            print("Error during LLM invoke:", e)
            return jsonify({"error": str(e)}), 500

@app.route('/summarize-email', methods=['POST'])
def summarize_email():
    data = request.get_json()
    received_email = data.get('received_email', '')

    if not received_email:
        return jsonify({"error": "No email provided"}), 400

    prompt = (
        f"You are an AI assistant. Provide a concise summary of the following email, highlighting the key points, "
        f"requests, and important information. Keep the summary brief but comprehensive.\n\n"
        f"Email:\n{received_email}\n\nSummary:"
    )

    try:
        response = llm.invoke(prompt)
        summary_text = response.content
        return jsonify({"summary": summary_text})

    except Exception as e:
        print("Error during email summarization:", e)
        return jsonify({"error": str(e)}), 500

# Tone rewriter endpoint removed as requested

@app.route('/generate-thread-reply', methods=['POST'])
def generate_thread_reply():
    data = request.get_json()
    email_thread = data.get('email_thread', [])
    tone = data.get('tone', 'professional')

    if not email_thread or not isinstance(email_thread, list) or len(email_thread) == 0:
        return jsonify({"error": "No email thread provided or invalid format"}), 400
    
    # Format the thread for the LLM
    formatted_thread = ""
    for i, email in enumerate(email_thread):
        formatted_thread += f"Email {i+1}:\n{email}\n\n"
    
    prompt = (
        f"You are an AI assistant. Below is an email thread with multiple messages. "
        f"Generate a reply to the most recent email in the thread, taking into account the entire conversation history. "
        f"The reply should be in a {tone} tone.\n\n"
        f"Email Thread:\n{formatted_thread}\n\n"
        f"Reply to the most recent email in the thread:"
    )

    try:
        response = llm.invoke(prompt)
        reply_text = response.content
        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Error during thread reply generation:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    received_email = data.get('received_email', '')

    if not received_email:
        return jsonify({"error": "No email provided"}), 400
    
    prompt = (
        f"You are an AI assistant. Analyze the sentiment of the following email and categorize it as one of the following: "
        f"positive, negative, neutral, or urgent. Also provide a brief explanation for your classification and suggest "
        f"an appropriate reply strategy based on the detected sentiment.\n\n"
        f"Email:\n{received_email}\n\n"
        f"Provide your response in JSON format with the following structure:\n"
        f"{{\n"
        f"  \"sentiment\": \"[sentiment category]\",\n"
        f"  \"explanation\": \"[brief explanation]\",\n"
        f"  \"reply_strategy\": \"[suggested reply approach]\"\n"
        f"}}\n"
    )

    try:
        response = llm.invoke(prompt)
        # Try to parse the response as JSON
        try:
            parsed_response = json.loads(response.content)
            return jsonify(parsed_response)
        except json.JSONDecodeError as e:
            print("Error parsing sentiment analysis response as JSON:", e)
            # If parsing fails, extract sentiment manually
            content = response.content.lower()
            
            # Determine sentiment based on content
            if "positive" in content:
                sentiment = "positive"
            elif "negative" in content:
                sentiment = "negative"
            elif "urgent" in content:
                sentiment = "urgent"
            else:
                sentiment = "neutral"
                
            # Create a structured response
            structured_response = {
                "sentiment": sentiment,
                "explanation": "Sentiment extracted from response text.",
                "reply_strategy": "Respond appropriately based on the detected sentiment."
            }
            
            return jsonify(structured_response)
    except Exception as e:
        print("Error during sentiment analysis:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/compose-email', methods=['POST'])
def compose_email():
    data = request.get_json()
    key_points = data.get('key_points', [])
    tone = data.get('tone', 'professional')
    
    if not key_points or len(key_points) == 0:
        return jsonify({"error": "No key points provided"}), 400
    
    # Format the key points for the LLM
    formatted_points = "\n".join([f"- {point}" for point in key_points])
    
    prompt = (
        f"You are an AI assistant. Compose a complete email based on the following key points. "
        f"The email should be in a {tone} tone and include all the information provided in the key points. "
        f"Make the email sound natural and well-structured with appropriate greetings and closing.\n\n"
        f"Key Points:\n{formatted_points}\n\n"
        f"Complete Email:"
    )

    try:
        response = llm.invoke(prompt)
        email_text = response.content
        return jsonify({"composed_email": email_text})

    except Exception as e:
        print("Error during email composition:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
