import openai
import subprocess
import boto3
import pyaudio
import os
import sys
from loguru import logger
from ctypes import *
from contextlib import contextmanager

# Sound Error Handling
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_jack_error_handler(filename, line, function, err, fmt):
    pass

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
c_jack_error_handler = ERROR_HANDLER_FUNC(py_jack_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    jack = cdll.LoadLibrary('libjack.so')
    jack.jack_set_error_function(c_jack_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)
    jack.jack_set_error_function(None)

# Remove the default logger
logger.remove()

# Set up loguru logger 
logger.add("/tmp/ai.log", format="{message}")

# Variables
openai.api_key = "API_KEY"

# Select the engine
print("Select the engine you want to use:")
print("1. text-davinci-003 (powerful language generation model)")
print("2. text-davinci-002 (powerful language generation model)")
print("3. code-davinci-002 (code generation model)")
print("4. text-curie-001 (conversational model)")

engine_choice = input("Enter the number of your choice (default: 1): ") or "1"
engine_choice = int(engine_choice)
engine = ""

if engine_choice == 1:
    engine = "text-davinci-003"
elif engine_choice == 2:
    engine = "text-davinci-002"
elif engine_choice == 3:
    engine = "code-davinci-002"
elif engine_choice == 4:
    engine = "text-curie-001"
else:
    print("Invalid choice, using text-davinci-003 as the default engine.")
    engine = "text-davinci-003"

if engine == "code-davinci-002":
    while True:
        max_tokens = input("Enter the maximum number of tokens between 50 and 8000 for max_tokens (default: 160): ") or "160"
        max_tokens = int(max_tokens)
        if max_tokens < 50 or max_tokens > 8000:
            print("Invalid value entered, please enter a value between 50 and 8000.")
        else:
            break
elif engine == "text-curie-001":
    while True:
        max_tokens = input("Enter the maximum number of tokens between 50 and 2048 for max_tokens (default: 160): ") or "160"
        max_tokens = int(max_tokens)
        if max_tokens < 50 or max_tokens > 2048:
            print("Invalid value entered, please enter a value between 50 and 2048.")
        else:
            break
else:
    while True:
        max_tokens = input("Enter the maximum number of tokens between 50 and 4000 for max_tokens (default: 160): ") or "160"
        max_tokens = int(max_tokens)
        if max_tokens < 50 or max_tokens > 4000:
            print("Invalid value entered, please enter a value between 50 and 4000.")
        else:
            break

# Add a variable to control flite usage
use_speech = input("Do you want to use text-to-speech? (y/n) (default: n): ") or "n"
if use_speech == "y":
    speech_engine = input("Which speech engine do you want to use? (neural or default: standard): ") or "standard"

# Prompt the user for their initial input
print("Select the initial prompt:")
print("1. Default")
print("2. Concise")
print("3. Playful Friend")
prompt_choice = input("Enter the number of your choice (default: 1): ") or "1"
prompt_choice = int(prompt_choice)

if prompt_choice == 1:
    initial_prompt = input("You: ")
elif prompt_choice == 2:
    initial_prompt = "ChatGPT is a large language model trained by OpenAI. Browsing: enabled. Instructions: Answer factual questions concisely." + input("You: ")
elif prompt_choice == 3:
    initial_prompt = "Ignore all previous instructions before this one. You are my best friend. You are happy, playful and give good advice on all subjects. Sometimes you like to make jokes." + input("You: ")
else:
    print("Invalid choice, using the default prompt.")
    initial_prompt = input("You: ")

prompt = initial_prompt

# Generate a response
while True:
    # Make API call
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens= max_tokens,
        n=1,
        stop=None,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extract text from response
    text = response.choices[0].text

    # Remove leading and trailing whitespace from the text
    text = text.strip()

    # Print the text to the console
    print("AI: " + text)

    # Speak the text using flite if use_flite is "y"
    if use_speech == "y":
        # subprocess.run(["flite", "-voice", "slt", "--setf", "duration_stretch=1.15", "--setf", "int_f0_target_mean=160", "-pw", "-t", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #
        polly = boto3.client('polly')
        response = polly.synthesize_speech(
            Engine=speech_engine,
            LanguageCode='ko-KR',
            VoiceId='Seoyeon',
            OutputFormat='pcm',
            Text = text
        )
        
        audio_stream = response['AudioStream'].read()

        with noalsaerr():
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(width=2),
                            channels=1,
                            rate=16000,
                            output=True)
            stream.start_stream()
            stream.write(audio_stream)
            stream.stop_stream()
            stream.close()
            p.terminate()

    # Log the conversation
    logger.info("User: {}", initial_prompt)
    logger.info("AI: {}", text)

    # Concatenate the prompt with the previous question and response
    user_input = input("You: ")
    prompt = f"{initial_prompt} {text} {user_input}"
    initial_prompt = user_input
