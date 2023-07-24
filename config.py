"""GPTInterface default config"""
APIKEYS = [""]                  # Your OpenAI API keys
MODEL = "gpt-3.5-turbo"         # GPT model name
LANGUAGE = "English"            # Only partially support Chinese
KEYWORD = "Science&Engineering" # Keyword for GPT model (What field you want the model to focus on)
PROXY = None                    # Your proxy address
# Note: If you are in China, you may need to use a proxy to access OpenAI API
# (If your system's global proxy is set, you can leave it as None)
# PROXY = "http://127.0.0.1:7890"  

# Max generation item number
TEXT2LIST_MAX_NUM = 4
TEXT2TREE_MAX_NUM = 4

if True: # Use true GPT model
    GPT_ENABLE = True
    THREAD_RATE_LIMIT = 3       # Each APIKEY can send 3 requests per minute (limited by OpenAI)
else:    # Use fake GPT model
    GPT_ENABLE = False
    THREAD_RATE_LIMIT = 600   
FAKE_GPT_RESPONSE = "FakeResponse"

