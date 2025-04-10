
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def generate_gherkin_langchain(user_story):
    llm = Ollama(model="mistral")
    template = PromptTemplate(
        input_variables=["story"],
        template="Convert the following user story into Gherkin format:

{story}"
    )
    chain = LLMChain(llm=llm, prompt=template)
    result = chain.run(story=user_story)
    return result
