# Aritificial Intelligence as Assistive Tech

## Setup Instructions

Install dependencies:

```
pip install openai tiktoken numpy os dotenv
```

## Create/Attach your OpenAI API Key

You'll need to create an OpenAI API key and add a few credits to run this code.
Create your OpenAI API Key: https://platform.openai.com/api-keys.

Create a `.env` file and add your API key to the file like this:

```
OPENAI_API_KEY="enter your key here"
```

## Run the file

Now, run your code:

```
python3 v0.py
```

And you should see:
![running screenshot](image.png)

## Next Steps:

- [ ] Add multiple files for context using the `embeddings` API: https://platform.openai.com/docs/guides/embeddings
- [ ] Read calendar `.ics` files
- [ ] Make it agentic?, use the Agents API: https://platform.openai.com/docs/guides/agents
- [ ] Prioritize context and tasks based on deadlines
- [ ] Decide what the interface should look like?
- [ ] Switch the AI provider... enable Claude
