import tomllib

from sapling_api import sapling_check
from ai21_api import ai21_check
from openai_api import openai_check
from opensource_api import opensourcellm_check
from constants import Tools

with open(
    r"F:\projects\freelancing\grammar-stuff\grammar_checker\.streamlit\secrets.toml",
    "rb",
) as f:
    SECRETS = tomllib.load(f)


def grammar_checker(iToolName, iText):
    corrected_text = ""
    match iToolName:
        case Tools.Sapling:
            corrected_text = sapling_check(SECRETS["SAPLING_API_KEY"], iText)

        case Tools.WordTune:
            corrected_text = ai21_check(SECRETS["AI21_API_KEY"], iText)

        case Tools.ChatGPT:
            corrected_text = openai_check(SECRETS["OPENAI_API_KEY"], iText)

        case Tools.OpenSourceLLM:
            corrected_text = opensourcellm_check(SECRETS["OPENROUTER_API_KEY"], iText)

    return corrected_text
