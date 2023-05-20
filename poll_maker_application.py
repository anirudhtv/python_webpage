import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define the session state variables
if "poll_questions" not in st.session_state:
    st.session_state.poll_questions = {}
if "poll_responses" not in st.session_state: 
    st.session_state.poll_responses = {}

# Define the poll questions screen
def poll_questions():
    st.header("Create a New Poll")
    question = st.text_input("Enter a poll question:")
    options = []
    for i in range(5):
        option = st.text_input(f"Option {i+1}:", key=f"option_{i}")
        if option:
            options.append(option)
    if st.button("Create Poll"):
        st.session_state.poll_questions[question] = options
        st.session_state.poll_responses[question] = {option: 0 for option in options}
        st.success("Poll created successfully!")

# Define the poll responses screen
def poll_responses():
    st.header("Vote on a Poll")
    question = st.selectbox("Select a poll question:", list(st.session_state.poll_questions.keys()))
    options = st.session_state.poll_questions[question]
    choice = st.radio("Select an option:", options)
    st.session_state.poll_responses[question][choice] += 1
    if st.button("submit"):
        st.success("Vote submitted successfully!")

# Define the poll results screen
def poll_results():
    st.header("View Poll Results")
    if not st.session_state.poll_responses:
        st.warning("No poll results to show")
        return
    question = st.selectbox("Select a poll question:", list(st.session_state.poll_questions.keys()))
    options = st.session_state.poll_questions[question]
    votes = [st.session_state.poll_responses[question][option] for option in options]
    fig, ax = plt.subplots()
    ax.bar(options, votes)
    ax.set_xlabel("Options")
    ax.set_ylabel("Votes")
    st.pyplot(fig)

# Define the save results screen
def save_results():
    st.header("Save Poll Results")
    if not st.session_state.poll_responses:
        st.warning("No poll results to save")
        return
    question = st.selectbox("Select a poll question:", list(st.session_state.poll_questions.keys()))
    options = st.session_state.poll_questions[question]
    votes = [st.session_state.poll_responses[question][option] for option in options]
    poll_results_df = pd.DataFrame({"Options": options, "Votes": votes})
    st.write(poll_results_df)
    filename = st.text_input("Enter a filename:")
    if st.button("Save Results"):
        poll_results_df.to_csv(filename, index=False)
        st.success(f"Results saved to {filename}!")

# Define the app layout and routing
st.set_page_config(page_title="Poll Maker App")
menu = ["Poll Questions", "Poll Responses", "Poll Results", "Save Results"]
choice = st.sidebar.selectbox("Select an option:", menu)
if choice == "Poll Questions":
    poll_questions()
elif choice == "Poll Responses":
    poll_responses()
elif choice == "Poll Results":
    poll_results()
else:
    save_results()