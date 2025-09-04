# import streamlit as st
# import requests

# st.set_page_config(page_title="Smart Email Assistant", layout="wide")

# # Create sidebar for navigation
# st.sidebar.title("📧 Email Assistant")
# page = st.sidebar.radio("Select Feature", ["Smart Reply", "Email Summary", "Thread Reply", "Sentiment Analysis", "Email Composer"])

# st.sidebar.markdown("---")
# st.sidebar.info("This application helps you manage emails with AI assistance.")

# # Main page content based on selection
# if page == "Smart Reply":
#     st.title("Smart Reply Generator")
#     st.markdown("Generate AI-powered replies to your emails with different tones.")
    
#     # Input received email
#     received_email = st.text_area("Paste the received email here", height=200, key="smart_reply_input")
    
#     # Options for reply generation
#     col1, col2, col3 = st.columns([2, 2, 1])
#     with col1:
#         tone = st.selectbox("Choose tone of reply", ["Formal", "Friendly", "Apologetic", "Assertive", "Neutral"])
#     with col2:
#         generate_multiple = st.checkbox("Generate multiple reply options", value=True)
#     with col3:
#         if st.button("Clear Input", key="clear_smart_reply"):
#             st.session_state["smart_reply_input"] = ""
#             st.rerun()
    
#     if st.button("Generate Reply"):
#         if not received_email:
#             st.warning("Please paste an email to reply to.")
#         else:
#             with st.spinner("Generating reply options..."):
#                 response = requests.post(
#                     "http://127.0.0.1:5000/generate-reply",
#                     json={
#                         "received_email": received_email, 
#                         "tone": tone.lower(),
#                         "generate_multiple": generate_multiple
#                     }
#                 )
                
#                 if response.status_code == 200:
#                     data = response.json()
                    
#                     if generate_multiple and "replies" in data:
#                         st.success("Multiple reply options generated!")
                        
#                         # Display each reply option in an expander
#                         replies = data["replies"]
#                         selected_reply = None
                        
#                         for i, reply_data in enumerate(replies):
#                             reply_tone = reply_data["tone"]
#                             reply_text = reply_data["reply"]
#                             with st.expander(f"Option {i+1}: {reply_tone.capitalize()} Reply", expanded=(i==0)):
#                                 st.text_area(f"Reply Option {i+1}", value=reply_text, height=150, key=f"reply_{i}")
#                                 if st.button(f"Select this reply", key=f"select_{i}"):
#                                     selected_reply = reply_text
                        
#                         if selected_reply:
#                             st.session_state.selected_reply = selected_reply
#                             st.success("Reply selected! You can now copy it or further modify it.")
#                             st.text_area("Selected Reply", value=selected_reply, height=200)
#                     else:
#                         # Single reply
#                         reply = data.get("reply")
#                         st.success("Reply generated:")
#                         st.text_area("Generated Reply", value=reply, height=200)
#                 else:
#                     st.error("Failed to connect to backend or generate reply.")

# elif page == "Email Summary":
#     st.title("Email Summarization")
#     st.markdown("Get concise summaries of long emails to quickly understand the key points.")
    
#     # Input received email for summarization
#     summary_email = st.text_area("Paste the email you want to summarize", height=200, key="summary_input")
    
#     # Add clear button
#     if st.button("Clear Input", key="clear_summary"):
#         st.session_state["summary_input"] = ""
#         st.rerun()
    
#     if st.button("Summarize Email"):
#         if not summary_email:
#             st.warning("Please paste an email to summarize.")
#         else:
#             with st.spinner("Generating summary..."):
#                 response = requests.post(
#                     "http://127.0.0.1:5000/summarize-email",
#                     json={"received_email": summary_email}
#                 )
                
#                 if response.status_code == 200:
#                     summary = response.json().get("summary")
#                     st.success("Email summarized!")
                    
#                     # Display the original email and summary side by side
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         st.subheader("Original Email")
#                         st.text_area("Original", value=summary_email, height=150, disabled=True)
#                     with col2:
#                         st.subheader("Summary")
#                         st.text_area("Summarized Content", value=summary, height=150)
#                 else:
#                     st.error("Failed to connect to backend or generate summary.")

# elif page == "Thread Reply":
#     st.title("Context-Aware Thread Reply")
#     st.markdown("Generate replies that take into account the full context of an email thread.")
    
#     # Initialize session state for email thread if it doesn't exist
#     if 'email_thread' not in st.session_state:
#         st.session_state.email_thread = []
    
#     # Display current thread
#     if st.session_state.email_thread:
#         st.subheader("Current Email Thread")
#         for i, email in enumerate(st.session_state.email_thread):
#             with st.expander(f"Email {i+1}", expanded=False):
#                 st.text_area(f"Email content {i+1}", value=email, height=100, disabled=True, key=f"thread_{i}")
#     else:
#         st.info("No emails in the thread yet. Add emails below to create a thread.")
    
#     # Add new email to thread
#     new_thread_email = st.text_area("Add email to thread", height=150)
#     if st.button("Add to Thread"):
#         if new_thread_email:
#             st.session_state.email_thread.append(new_thread_email)
#             st.success("Email added to thread!")
#             st.rerun()
#         else:
#             st.warning("Please enter an email to add to the thread.")
    
#     # Clear thread button
#     if st.button("Clear Thread"):
#         st.session_state.email_thread = []
#         st.success("Thread cleared!")
#         st.rerun()
    
#     # Generate reply based on thread
#     if st.session_state.email_thread:
#         st.subheader("Generate Reply to Thread")
#         thread_tone = st.selectbox("Choose tone for thread reply", 
#                                 ["Professional", "Formal", "Friendly", "Concise"], key="thread_tone")
        
#         if st.button("Generate Thread Reply"):
#             with st.spinner("Analyzing thread and generating reply..."):
#                 response = requests.post(
#                     "http://127.0.0.1:5000/generate-thread-reply",
#                     json={
#                         "email_thread": st.session_state.email_thread,
#                         "tone": thread_tone.lower()
#                     }
#                 )
                
#                 if response.status_code == 200:
#                     thread_reply = response.json().get("reply")
#                     st.success("Thread reply generated!")
#                     st.text_area("Generated Reply", value=thread_reply, height=200)
#                 else:
#                     st.error("Failed to connect to backend or generate thread reply.")

# elif page == "Email Composer":
#     st.title("Email Composer")
#     st.markdown("Generate a complete email based on key points you provide.")
    
#     # Initialize session state for key points if it doesn't exist
#     if 'key_points' not in st.session_state:
#         st.session_state.key_points = [""]
    
#     # Email tone selection
#     email_tone = st.selectbox("Choose email tone", 
#                            ["Professional", "Formal", "Friendly", "Casual", "Enthusiastic", 
#                             "Apologetic", "Assertive", "Empathetic", "Concise", "Detailed"],
#                            key="email_tone")
    
#     # Key points input
#     st.subheader("Enter Key Points")
#     st.markdown("Add the main points you want to include in your email.")
    
#     # Display existing key points with option to edit
#     for i, point in enumerate(st.session_state.key_points):
#         col1, col2 = st.columns([10, 1])
#         with col1:
#             st.session_state.key_points[i] = st.text_input(f"Point {i+1}", value=point, key=f"point_{i}")
#         with col2:
#             if st.button("❌", key=f"remove_{i}") and len(st.session_state.key_points) > 1:
#                 st.session_state.key_points.pop(i)
#                 st.rerun()
    
#     # Add new key point button
#     if st.button("Add Another Point"):
#         st.session_state.key_points.append("")
#         st.rerun()
    
#     # Clear all points button
#     if st.button("Clear All Points"):
#         st.session_state.key_points = [""]
#         st.rerun()
    
#     # Generate email button
#     if st.button("Generate Email"):
#         # Filter out empty key points
#         key_points = [point for point in st.session_state.key_points if point.strip()]
        
#         if not key_points:
#             st.warning("Please add at least one key point.")
#         else:
#             with st.spinner("Composing your email..."):
#                 response = requests.post(
#                     "http://127.0.0.1:5000/compose-email",
#                     json={
#                         "key_points": key_points,
#                         "tone": email_tone.lower()
#                     }
#                 )
                
#                 if response.status_code == 200:
#                     composed_email = response.json().get("composed_email")
#                     st.success("Email composed successfully!")
                    
#                     # Display the composed email
#                     st.subheader("Generated Email")
#                     st.text_area("Composed Email", value=composed_email, height=300)
                    
#                     # Add a button to copy the email
#                     if st.button("Copy to Clipboard"):
#                         st.session_state.selected_reply = composed_email
#                         st.success("Email copied to clipboard!")
#                 else:
#                     st.error("Failed to connect to backend or compose email.")

# elif page == "Sentiment Analysis":
#     st.title("Email Sentiment Analysis")
#     st.markdown("Analyze the sentiment of emails to better understand the sender's tone and intent.")
    
#     # Input email for sentiment analysis
#     sentiment_email = st.text_area("Paste the email you want to analyze", height=200, key="sentiment_input")
    
#     # Add clear button
#     if st.button("Clear Input", key="clear_sentiment"):
#         st.session_state["sentiment_input"] = ""
#         st.rerun()
        
#     if st.button("Analyze Sentiment"):
#         if not sentiment_email:
#             st.warning("Please paste an email to analyze.")
#         else:
#             with st.spinner("Analyzing email sentiment..."):
#                 response = requests.post(
#                     "http://127.0.0.1:5000/analyze-sentiment",
#                     json={"received_email": sentiment_email}
#                 )
                
#                 if response.status_code == 200:
#                     analysis = response.json()
                    
#                     # Display sentiment analysis results
#                     st.success("Sentiment analysis complete!")
                    
#                     # Create columns for sentiment display
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         # Display sentiment with appropriate color
#                         sentiment = analysis.get("sentiment", "unknown")
#                         sentiment_color = {
#                             "positive": "#28a745",  # green
#                             "negative": "#dc3545",  # red
#                             "neutral": "#6c757d",   # gray
#                             "urgent": "#ffc107"     # yellow/amber
#                         }.get(sentiment.lower(), "#6c757d")
                        
#                         st.markdown(f"<h3 style='color: {sentiment_color}'>Sentiment: {sentiment.upper()}</h3>", unsafe_allow_html=True)
#                         st.markdown(f"**Explanation:** {analysis.get('explanation', '')}")
                    
#                     with col2:
#                         st.subheader("Suggested Reply Strategy")
#                         st.info(analysis.get("reply_strategy", ""))
                    
#                     # Display the original email below
#                     st.subheader("Original Email")
#                     st.text_area("Email Content", value=sentiment_email, height=150, disabled=True)
                    
#                 else:
#                     st.error("Failed to connect to backend or analyze sentiment.")

import streamlit as st
import requests

st.set_page_config(page_title="Smart Email Assistant", layout="wide")

# Initialize session state keys safely
for key in ["smart_reply_input", "summary_input", "sentiment_input"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# Create sidebar for navigation
st.sidebar.title("📧 Email Assistant")
page = st.sidebar.radio("Select Feature", ["Smart Reply", "Email Summary", "Thread Reply", "Sentiment Analysis", "Email Composer"])

st.sidebar.markdown("---")
st.sidebar.info("This application helps you manage emails with AI assistance.")

# Main page content based on selection
if page == "Smart Reply":
    st.title("Smart Reply Generator")
    st.markdown("Generate AI-powered replies to your emails with different tones.")
    
    # Input received email
    received_email = st.text_area("Paste the received email here", height=200, key="smart_reply_input")
    
    # Options for reply generation
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        tone = st.selectbox("Choose tone of reply", ["Formal", "Friendly", "Apologetic", "Assertive", "Neutral"])
    with col2:
        generate_multiple = st.checkbox("Generate multiple reply options", value=True)
    with col3:
        if st.button("Clear Input", key="clear_smart_reply"):
            st.rerun()
    
    if st.button("Generate Reply"):
        if not received_email:
            st.warning("Please paste an email to reply to.")
        else:
            with st.spinner("Generating reply options..."):
                response = requests.post(
                    "http://127.0.0.1:5000/generate-reply",
                    json={
                        "received_email": received_email, 
                        "tone": tone.lower(),
                        "generate_multiple": generate_multiple
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if generate_multiple and "replies" in data:
                        st.success("Multiple reply options generated!")
                        
                        # Display each reply option in an expander
                        replies = data["replies"]
                        selected_reply = None
                        
                        for i, reply_data in enumerate(replies):
                            reply_tone = reply_data["tone"]
                            reply_text = reply_data["reply"]
                            with st.expander(f"Option {i+1}: {reply_tone.capitalize()} Reply", expanded=(i==0)):
                                st.text_area(f"Reply Option {i+1}", value=reply_text, height=150, key=f"reply_{i}")
                                if st.button(f"Select this reply", key=f"select_{i}"):
                                    selected_reply = reply_text
                        
                        if selected_reply:
                            st.session_state.selected_reply = selected_reply
                            st.success("Reply selected! You can now copy it or further modify it.")
                            st.text_area("Selected Reply", value=selected_reply, height=200)
                    else:
                        # Single reply
                        reply = data.get("reply")
                        st.success("Reply generated:")
                        st.text_area("Generated Reply", value=reply, height=200)
                else:
                    st.error("Failed to connect to backend or generate reply.")

elif page == "Email Summary":
    st.title("Email Summarization")
    st.markdown("Get concise summaries of long emails to quickly understand the key points.")
    
    # Input received email for summarization
    summary_email = st.text_area("Paste the email you want to summarize", height=200, key="summary_input")
    
    # Add clear button
    def clear_summary():
        st.session_state["summary_input"] = ""
    st.button("Clear Input", key="clear_summary", on_click=clear_summary)
    
    if st.button("Summarize Email"):
        if not summary_email:
            st.warning("Please paste an email to summarize.")
        else:
            with st.spinner("Generating summary..."):
                response = requests.post(
                    "http://127.0.0.1:5000/summarize-email",
                    json={"received_email": summary_email}
                )
                
                if response.status_code == 200:
                    summary = response.json().get("summary")
                    st.success("Email summarized!")
                    
                    # Display the original email and summary side by side
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Original Email")
                        st.text_area("Original", value=summary_email, height=150, disabled=True)
                    with col2:
                        st.subheader("Summary")
                        st.text_area("Summarized Content", value=summary, height=150)
                else:
                    st.error("Failed to connect to backend or generate summary.")

elif page == "Thread Reply":
    st.title("Context-Aware Thread Reply")
    st.markdown("Generate replies that take into account the full context of an email thread.")
    
    # Initialize session state for email thread if it doesn't exist
    if 'email_thread' not in st.session_state:
        st.session_state.email_thread = []
    
    # Display current thread
    if st.session_state.email_thread:
        st.subheader("Current Email Thread")
        for i, email in enumerate(st.session_state.email_thread):
            with st.expander(f"Email {i+1}", expanded=False):
                st.text_area(f"Email content {i+1}", value=email, height=100, disabled=True, key=f"thread_{i}")
    else:
        st.info("No emails in the thread yet. Add emails below to create a thread.")
    
    # Add new email to thread
    new_thread_email = st.text_area("Add email to thread", height=150)
    if st.button("Add to Thread"):
        if new_thread_email:
            st.session_state.email_thread.append(new_thread_email)
            st.success("Email added to thread!")
            st.rerun()
        else:
            st.warning("Please enter an email to add to the thread.")
    
    # Clear thread button
    if st.button("Clear Thread"):
        st.session_state.email_thread = []
        st.success("Thread cleared!")
        st.rerun()
    
    # Generate reply based on thread
    if st.session_state.email_thread:
        st.subheader("Generate Reply to Thread")
        thread_tone = st.selectbox("Choose tone for thread reply", 
                                ["Professional", "Formal", "Friendly", "Concise"], key="thread_tone")
        
        if st.button("Generate Thread Reply"):
            with st.spinner("Analyzing thread and generating reply..."):
                response = requests.post(
                    "http://127.0.0.1:5000/generate-thread-reply",
                    json={
                        "email_thread": st.session_state.email_thread,
                        "tone": thread_tone.lower()
                    }
                )
                
                if response.status_code == 200:
                    thread_reply = response.json().get("reply")
                    st.success("Thread reply generated!")
                    st.text_area("Generated Reply", value=thread_reply, height=200)
                else:
                    st.error("Failed to connect to backend or generate thread reply.")

elif page == "Email Composer":
    st.title("Email Composer")
    st.markdown("Generate a complete email based on key points you provide.")
    
    # Initialize session state for key points if it doesn't exist
    if 'key_points' not in st.session_state:
        st.session_state.key_points = [""]
    
    # Email tone selection
    email_tone = st.selectbox("Choose email tone", 
                           ["Professional", "Formal", "Friendly", "Casual", "Enthusiastic", 
                            "Apologetic", "Assertive", "Empathetic", "Concise", "Detailed"],
                           key="email_tone")
    
    # Key points input
    st.subheader("Enter Key Points")
    st.markdown("Add the main points you want to include in your email.")
    
    # Display existing key points with option to edit
    for i, point in enumerate(st.session_state.key_points):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.session_state.key_points[i] = st.text_input(f"Point {i+1}", value=point, key=f"point_{i}")
        with col2:
            if st.button("❌", key=f"remove_{i}") and len(st.session_state.key_points) > 1:
                st.session_state.key_points.pop(i)
                st.rerun()
    
    # Add new key point button
    if st.button("Add Another Point"):
        st.session_state.key_points.append("")
        st.rerun()
    
    # Clear all points button
    if st.button("Clear All Points"):
        st.session_state.key_points = [""]
        st.rerun()
    
    # Generate email button
    if st.button("Generate Email"):
        # Filter out empty key points
        key_points = [point for point in st.session_state.key_points if point.strip()]
        
        if not key_points:
            st.warning("Please add at least one key point.")
        else:
            with st.spinner("Composing your email..."):
                response = requests.post(
                    "http://127.0.0.1:5000/compose-email",
                    json={
                        "key_points": key_points,
                        "tone": email_tone.lower()
                    }
                )
                
                if response.status_code == 200:
                    composed_email = response.json().get("composed_email")
                    st.success("Email composed successfully!")
                    
                    # Display the composed email
                    st.subheader("Generated Email")
                    st.text_area("Composed Email", value=composed_email, height=300, key="copy_target")
                else:
                    st.error("Failed to connect to backend or compose email.")

elif page == "Sentiment Analysis":
    st.title("Email Sentiment Analysis")
    st.markdown("Analyze the sentiment of emails to better understand the sender's tone and intent.")
    
    # Input email for sentiment analysis
    sentiment_email = st.text_area("Paste the email you want to analyze", height=200, key="sentiment_input")
    
    # Add clear button
    def clear_sentiment():
        st.session_state["sentiment_input"] = ""
    st.button("Clear Input", key="clear_sentiment", on_click=clear_sentiment)
        
    if st.button("Analyze Sentiment"):
        if not sentiment_email:
            st.warning("Please paste an email to analyze.")
        else:
            with st.spinner("Analyzing email sentiment..."):
                response = requests.post(
                    "http://127.0.0.1:5000/analyze-sentiment",
                    json={"received_email": sentiment_email}
                )
                
                if response.status_code == 200:
                    analysis = response.json()
                    
                    # Display sentiment analysis results
                    st.success("Sentiment analysis complete!")
                    
                    # Create columns for sentiment display
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Display sentiment with appropriate color
                        sentiment = analysis.get("sentiment", "unknown")
                        sentiment_color = {
                            "positive": "#28a745",  # green
                            "negative": "#dc3545",  # red
                            "neutral": "#6c757d",   # gray
                            "urgent": "#ffc107"     # yellow/amber
                        }.get(sentiment.lower(), "#6c757d")
                        
                        st.markdown(f"<h3 style='color: {sentiment_color}'>Sentiment: {sentiment.upper()}</h3>", unsafe_allow_html=True)
                        st.markdown(f"**Explanation:** {analysis.get('explanation', '')}")
                    
                    with col2:
                        st.subheader("Suggested Reply Strategy")
                        st.info(analysis.get("reply_strategy", ""))
                    
                    # Display the original email below
                    st.subheader("Original Email")
                    st.text_area("Email Content", value=sentiment_email, height=150, disabled=True)
                    
                else:
                    st.error("Failed to connect to backend or analyze sentiment.")
