Welcome to the OpenAI command line tool! 🚀

This script allows you to generate text or code using the OpenAI API. 

Here's how to use it:

1. Run the script on your command line.

2. Select one of the four available engines: text-davinci-003, text-davinci-002, code-davinci-002, or text-curie-001.

3. Enter the maximum number of tokens you want the output to have. The range of maximum token count is between 50 and 4000 for text-davinci-003 and text-davinci-002, 50 to 8000 for code-davinci-002, and 50 to 2048 for text-curie-001.

4. Choose if you want to use text-to-speech by typing 'y' for yes or 'n' for no.

5. The script will now generate output for you.

Please note: 
- You must add your own API key to use the script.
- The script uses several other libraries including subprocess, boto3, pyaudio, os, sys, and loguru.
- The script also has error handling implemented for sound errors.
- The script log the messages to a file "/tmp/ai.log"
- AWS Polly is used for speech and requires API Keys already setup.

Enjoy using the power of OpenAI!
