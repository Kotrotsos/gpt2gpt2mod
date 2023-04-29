# GPT2GPT

This script simulates a chat between 2 participants. (By default Alice and Bob) about a certain topic. A moderator is included in the conversation to keep it on track.

Upon execution the system will ask for a topic to discuss. On subsequent runs it will remember the previous topic. 

To run:

Add the OpenAI API key to the environment variable OPENAI_API_KEY. On linux/MacOS

``` export OPENAI_API_KEY=<yourkeyhere> ```

On windows

``` setx OPENAI_API_KEY "<yourkeyhere>" ```

To run the script

``` python gpt2gpt.py -p Bob:Alice ```

or

``` python gpt2gpt.py --h ```

For command line parameters.

The script will run autonomously. So be mindful about this that it can increase your token spent substantially. The model is GPT-3.5-turbo by default. Remember, GPT-4 is 10x more expensive. 

Also please note, The discussion can (most likely will) go off the rails regarding who is discussing what at a particular moment. Also- the model is prone to fall into a 'Goodbye thank you' loop. The moderator is there to keep it on track somewhat. But- it's not very clever yet. The moderator will get more tasks in the future as well. Like acting more as an intelligent agent than just to moderate the conversation and keep it going. 

Added Agent role to start investigating a role specifically to keep track of tasks to perform. The moderator is there to keep the conversation going, the Agent to see if more help is needed.

## TODO

- Moderator ending the conversation
- Moderator being assigned tasks like fetching information off the web.
- Better prompting mechanism
- Keep track off who is talking when. 
