import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions.kernel_function_from_prompt import KernelFunctionFromPrompt
from semantic_kernel.core_plugins import TextPlugin
from semantic_kernel.kernel import KernelArguments
from dotenv import load_dotenv
load_dotenv()
import asyncio

kernel = Kernel()

api_key = os.environ.get('OPENAI_API_KEY')

chat_service = OpenAIChatCompletion(
    ai_model_id="gpt-4o-mini-2024-07-18",
    api_key=api_key
)
kernel.add_service(chat_service)

with open("skagent/functions/extract_space_and_message_prompt.yaml", "r") as f:
    yaml_content = f.read()
        
userInputFunction = KernelFunctionFromPrompt.from_yaml(yaml_str=yaml_content,plugin_name="userInputPlugin")
kernel.add_function(plugin_name="userInputPlugin",function=userInputFunction)

"""
async def debug_render():
    args = KernelArguments(input="Give me the total counts of Empty or Blanks for Gender for dataset avrodatasource, my space id is 01f01e2d8e1d1087a9e7186c76e64ed0")
    rendered = await userInputFunction.prompt_template.render(kernel, args)
    print(rendered)

asyncio.run(debug_render())
"""

with open("skagent/functions/summarize_result_prompt.yaml", "r") as f:
    yaml_content = f.read()

userOutputFunction = KernelFunctionFromPrompt.from_yaml(yaml_str=yaml_content,plugin_name="userOutputPlugin")
kernel.add_function(plugin_name="userOutputPlugin",function=userOutputFunction)


#async def debug_render():
#    input_str = str("""{"result": {"conversation_id": "01f01fb69b451b79b1d2d50102fac9ec", "message_id": "01f01fb69b5e176aa3068409ebf5b221", "content": "Total counts of Empty or Blanks for Gender in dataset avrodatasource", "status": "COMPLETED", "attachments": [{"attachment_id": "01f01fb69d9c128c91f3b5c38c22395a", "query": {"description": "This query provides the total number of entries in the dataset where the gender information is either missing or not specified.", "query": "SELECT COUNT(*) FROM `main`.`ucdevdb`.`avrodatasource` WHERE `gender` IS NULL OR `gender` = ''", "query_result_metadata": {"row_count": 1}, "statement_id": "01f01fb6-9daa-17b1-8a1c-9f07cd8f0b54"}}]}, "query_result": {"manifest": {"chunks": [{"byte_count": 328, "chunk_index": 0, "row_count": 1, "row_offset": 0}], "format": "JSON_ARRAY", "schema": {"column_count": 1, "columns": [{"name": "count(1)", "position": 0, "type_name": "LONG", "type_text": "BIGINT"}]}, "total_byte_count": 328, "total_chunk_count": 1, "total_row_count": 1, "truncated": false}, "result": {"chunk_index": 0, "data_array": [["59"]], "row_count": 1, "row_offset": 0}, "statement_id": "01f01fb6-9daa-17b1-8a1c-9f07cd8f0b54", "status": {"state": "SUCCEEDED"}}}""")
#    args = KernelArguments(input=input_str)
#    rendered = await userOutputFunction.prompt_template.render(kernel, args)
#    print(rendered)

#asyncio.run(debug_render())
