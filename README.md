# README

Are you ready to have some fun with OpenAI? Then, this script is for you!
This script is a simple command-line interface that uses the OpenAI API to generate responses to user input, like a real-life AI chatbot.

Here are some of the features of this script:
- It allows you to select the engine you want to use from 4 options:
    1. text-davinci-003 (powerful language generation model)
    2. text-davinci-002 (powerful language generation model)
    3. code-davinci-002 (code generation model)
    4. text-curie-001 (conversational model)
- It uses loguru to log the conversation
- It uses flite to speak the response of AI.
- It allows you to set the max_tokens for the API call.
- It goes into a loop where it waits for your input, generates a response using the OpenAI API, and speaks the response using flite.
- The script will keep running until you stop it.

You will need to have `openai` and `loguru` python packages installed to run this script.
You will need to add your own OpenAI API key to the script before running it.

Note: flite is a small text-to-speech engine, if you don't have flite installed in your system, you can remove the line of code where it is used to speak the text.

This script is under the MIT License.

The MIT License is a permissive open-source license that allows you to use, modify, and redistribute the software and source code with or without modification. You can read more about the MIT License here: https://opensource.org/licenses/MIT

Useful links:
- OpenAI API: https://beta.openai.com/
- ChatGPT FAQ: https://beta.openai.com/docs/models/gpt-3#faq
