import json
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain

# Load model.json
with open("model.json") as f:
    model_config = json.load(f)

# Set up LLM
llm = Ollama(model="llama3")  # Replace with your installed model if needed

# Prompt Template
template = """
You are a CI/CD config expert. Here is the model config:

{model_config}

Check the following Dockerfile content:

{dockerfile_content}

Do the following:
- Check if all required keys like EXPOSE, CMD exist.
- Identify drift from model.
- Suggest exact line changes to make it compliant.

Return fix plan in Markdown.
"""

prompt = PromptTemplate.from_template(template)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_parser=StrOutputParser()
)

# Load Dockerfile
dockerfile_path = Path(model_config['services']['api']['dockerfile'])
dockerfile_content = dockerfile_path.read_text()

# Call Agent
response = chain.invoke({
    "model_config": json.dumps(model_config, indent=2),
    "dockerfile_content": dockerfile_content
})

print("🔧 Fix Plan:\n")
print(response)
