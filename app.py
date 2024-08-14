import streamlit as st
import random
import re


# List of 5-letter words
word_list = [
    "apple", "grape", "pearl", "flame", "stone",
    "ocean", "brave", "crane", "plume", "spark",
    "blaze", "globe", "quest", "vivid", "prism",
    "frost", "clock", "honey", "maple", "whale",
    "daisy", "shark", "charm", "smile", "peach",
    "cloud", "drift", "creek", "flour", "flock",
    "grove", "haunt", "jolly", "knack", "lemon",
    "lunar", "mango", "night", "olive", "piano",
    "quilt", "raven", "scout", "swirl", "tango",
    "unite", "vapor", "whirl", "xenon", "yacht",
    "zebra", "amber", "brick", "cedar", "dwell",
    "fable", "gleam", "haven", "ivory", "jazzy",
    "karma", "latte", "medal", "noble", "orbit",
    "petal", "quack", "reign", "spike", "truce",
    "umbra", "valor", "whisk", "xylem", "yeast",
    "zesty", "abode", "broil", "cling", "dunce",
    "ember", "frost", "glare", "hiker", "inbox",
    "jiffy", "knoll", "lilac", "mirth", "niece",
    "opine", "pluck", "quill", "rouge", "stark",
    "throb", "usher", "vista", "wrath", "xenon"
]


def reinitialize_game():
    st.session_state['game_active'] = True
    st.session_state['target_word'] = random.choice(word_list)
    st.session_state['attempts'] = []
    st.session_state['score'] = 0


def initialize_game():
    if 'target_word' not in st.session_state:
        st.session_state['target_word'] = random.choice(word_list)
    if 'attempts' not in st.session_state:
        st.session_state['attempts'] = []
    if 'game_active' not in st.session_state:
        st.session_state['game_active'] = False
    if 'score' not in st.session_state:
        st.session_state['score'] = 0

    st.title('Wordle game')
    st.sidebar.write(f"**Score:** {st.session_state['score']}")


def calculate_score(attempt_number):
    score = 100 * (1/2) ** (attempt_number - 1) if attempt_number <= 5 else 0
    return score


def is_valid_word(word):
    return bool(re.match("^[a-zA-Z]{5}$", word))


def give_feedback(str1, str2):
    if str1[i] == str2[i]:
        feedback = "🟩"  # correct letter and position
    elif str1[i] in str2:
        feedback = "🟨"  # correct letter but wrong position
    else:
        feedback = "⬛"  # letter not in word
    return feedback


def lose_actions():
    st.session_state['game_active'] = False
    st.write(f"**Game over!** You've reached the maximum number of \
                 attempts. The answer is **{target.upper()}**")
    st.session_state['score'] += calculate_score(len(attempts))
    st.button("Restart Game")  # Allow restart


def win_actions():
    st.write(f"**YOU WIN!** The answer was **{target.upper()}**.")
    st.session_state['score'] += calculate_score(len(attempts))
    st.button("Restart Game")  # Allow restart


def giveup_actions():
    st.write(f"**You gave up!** The answer was **{target.upper()}**.")
    st.session_state['score'] += calculate_score(len(attempts))
    st.session_state['game_active'] = False
    st.button("Restart Game")  # Allow restart


def answer_str(target):
    return f'The answer was **{target.upper()}**.'

# ======================================================
# MAIN


initialize_game()

# Handle game logic
if st.session_state['game_active']:
    target = st.session_state['target_word']
    attempts = st.session_state['attempts']

    # Limit to 6 attempts
    if len(attempts) >= 6:
        lose_actions()

    input_word = st.text_input("**Enter your 5-letter word guess:**",
                               max_chars=5,
                               placeholder="e.g. apple",
                               label_visibility="visible")

    input_word = input_word.lower()

    if st.button("Submit"):
        if len(input_word) == 5 and is_valid_word(input_word):
            attempts.append(input_word)
        elif not is_valid_word(input_word):
            st.write("**Invalid input! Please enter a 5-letter word.**")

    # Display guesses and feedback
    for attempt in attempts:
        feedback = ""
        for i in range(5):
            feedback += give_feedback(attempt, target)

        st.write(f"{attempt.upper()} {feedback}")

        if feedback == "🟩" * 5:
            win_actions()
            break

    # Button to give up
    if st.button("Give Up"):
        giveup_actions()

else:
    if st.button("Play the game"):
        reinitialize_game()
        st.write("**Game has started! Press the button again.**")
