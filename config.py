"""OpenAI API"""
APIBASE = ""                    # OpenAI API base, default is "https://api.openai.com/v1" for now (Leave it as empty if you are not sure)
APIKEYS = [""]                  # Your OpenAI API keys
MODEL = "gpt-3.5-turbo"         # GPT model name
MAXTOKEN = 4000                 # Max token number for each request (Cutoff is performed when the number of tokens exceeds this value)
LANGUAGE = "English"            # Only partially support Chinese
KEYWORD = "Science&Engineering" # Keyword for GPT model (What field you want the model to focus on)
PROXY = None                    # Your proxy address
# Note: If you are in China, you may need to use a proxy to access OpenAI API
# (If your system's global proxy is set, you can leave it as None)
# PROXY = "http://127.0.0.1:7890"


"""Generation"""
GEN_IMGS = True
GEN_EQUATIONS = True

# PDFFigure2
USE_PDFFIGURE2 = True       # Use PDFFigure2 to generate images & tables (This requires you to install JVM)
SNAP_WITH_CAPTION = True    # Generate images & tables with caption (Only valid when USE_PDFFIGURE2 is True)

# Max generation item number
TEXT2LIST_MAX_NUM = 4       # Max number of items for each list
TEXT2TREE_MAX_NUM = 4       # Max number of subtopics for each topic
FAKE_GPT_RESPONSE = "Fake"  # Fake GPT response when GPT_ENABLE is False
if True:  # Use true GPT model
    GPT_ENABLE = True
    THREAD_RATE_LIMIT = 100       # Each APIKEY can send 3 requests per minute (limited by OpenAI)
else:    # Use fake GPT model
    GPT_ENABLE = False
    THREAD_RATE_LIMIT = 6000


"""PDF Parser - Regular Expression"""
# Special title
ABS_MATCHSTR = "ABSTRACT|Abstract|abstract"
INTRO_MATCHSTR = "I.[\s]{1,3}(INTRODUCTION|Introduction|introduction)"
REF_MATCHSTR = "Reference|REFERENCE|Bibliography"
APD_MATCHSTR = "APPENDIX|Appendix"  # Not used for now
# General title
# FIXME: Misidentification exists
SECTION_TITLE_MATCHSTR = ["[IVX1-9]{1,4}[\.\s][\sA-Za-z]{1,}|[1-9]{1,2}[\s\.\n][\sA-Za-z]{1,}",  # Level 1
                          "[A-M]{1}\.[\sA-Za-z]{1,}|[1-9]\.[1-9]\.[\sA-Za-z]{1,}"]  # Level 2
# Equation & Image
EQUATION_MATCHSTR = '[\s]{0,}\([\d]{1,}[a-zA-Z]{0,1}\)'
IMG_MATCHSTR = 'Fig.[\s]{1,3}[\d]{1,2}|Figure[\s]{1,3}[\d]{1,2}|Tab.[\s]{1,3}[\dIVX]{1,3}|Table[\s]{1,3}[\dIVX]{1,3}'  # Figure & Table


"""Xmind Sytle Template"""
TEMPLATE_XMIND_PATH = 'template.xmind'


"""Debuging"""
DEBUG_MODE = False
