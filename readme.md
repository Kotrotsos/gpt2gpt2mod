#GPT2GPT

This script simulates a chat between 2 participants. (By default Alice and Bob) about a certain topic. 

Upon execution the system asks for a topic to discuss. On subsequent runs it will remember the previous topic. 

To run:

Add the OpenAI API key to the environment variable OPENAI_API_KEY. On linux/OsX

``` export OPENAI_API_KEY=<yourkeyhere> ```

The run the script

``` python gpt2gpt.py ```

or

``` python gpt2gpt.py --h ```

For command line parameters.

Please note, The discussion can go off the rails regarding who is discussing what at a particular moment. Also- the model is prone to fall into a 'Goodbye thank you' loop. The moderator is there to keep it on track somewhat. But- it's not very clever yet. The moderator will get more tasks in the future as well. Like acting more as an intelligent agent than just to moderate the conversation and keep it going. 

