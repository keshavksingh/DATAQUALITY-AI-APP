import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from semantic_kernel import Kernel
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.functions import KernelArguments
from semantic_kernel.kernel import KernelArguments
from skagent.kernel import kernel
from skagent.utils import extract_json_from_string
from dotenv import load_dotenv
import json
load_dotenv()

app = FastAPI()

class AssistantRequest(BaseModel):
    space_id: str
    message: str

class DataQualityAssistantRequest(BaseModel):
    message: str

#kernel: Kernel = None
#genie_plugin: MCPStdioPlugin = None

@app.on_event("startup")
async def startup_event():
    #global kernel, genie_plugin

    #kernel = Kernel()

    genie_plugin = MCPStdioPlugin(
    name="genie",
    description="Genie Tools",
    command="docker",
    args=[
        "exec", "-i",
        "-e", f"DATABRICKS_HOST={os.environ.get('DATABRICKS_HOST')}",
        "-e", f"DATABRICKS_TOKEN={os.environ.get('DATABRICKS_TOKEN')}",
        "mcpserver",
        "python", "/mcpserver/server.py"])
    
    print("Connecting to MCP Plugin...")
    await MCPStdioPlugin.connect(genie_plugin)
    print("MCP Plugin connected.")
    await genie_plugin.__aenter__()

    kernel.add_plugin(genie_plugin, plugin_name="genie")
    print(f"Plugins loaded: {kernel.plugins.keys()}")
    for plugin in kernel.plugins.keys():
    #if "genie" in kernel.plugins:
        #function_names = list(kernel.plugins["genie"].functions.keys())
        function_names = list(kernel.plugins[plugin].functions.keys())
        print(f"Plugin '{plugin}' Plugin functions: {function_names}")



@app.on_event("shutdown")
async def shutdown_event():
    global genie_plugin
    if genie_plugin:
        await genie_plugin.__aexit__(None, None, None)


@app.post("/assistant")
async def assistant(request: AssistantRequest):

    result = await kernel.invoke(
        plugin_name="genie",
        function_name="dataquality",
        space_id=request.space_id,
        content=request.message
    )

    return {
        "result": str(result)
    }

@app.post("/dataqualityassistant")
async def data_quality_assistant(request: DataQualityAssistantRequest):
    try:
        # 1. Call userInputFunction to extract space_id and message
        extraction_args = KernelArguments(input=request.message)
        extraction_result = await kernel.invoke(
            plugin_name="userInputPlugin",
            function_name="userInputFunction",
            arguments=extraction_args
        )

        print(f"Extraction Result: {extraction_result}")
        extracted_json_str = extract_json_from_string(str(extraction_result))
        print(f"Extraction Result in JSON : {extracted_json_str}")

        try:
            extraction_json = json.loads(extracted_json_str)
            space_id = extraction_json.get("space_id")
            message_to_dq = extraction_json.get("message")

            if not space_id or not message_to_dq:
                raise HTTPException(status_code=400, detail="Could not extract space_id and/or message from user input.")

            # 2. Call Data quality tool
            result = await kernel.invoke(
                plugin_name="genie",
                function_name="dataquality",
                space_id=space_id,
                content=message_to_dq
                )
            dq_response_json = str(result)
            print(f"DQ Raw Result:\n{dq_response_json}")

            # 3. Call userOutputFunction to format the result
            output_args = KernelArguments(input=dq_response_json)
            summary_result = await kernel.invoke(
                plugin_name="userOutputPlugin",
                function_name="userOutputFunction", 
                arguments=output_args
            )

            return {"result": str(summary_result)}

        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Error decoding JSON from userInputFunction.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing data quality request: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")



"""
@app.post("/assistant")
async def assistant(request: AssistantRequest):
    for plugin in kernel.plugins:
        print(f"Plugin: {plugin}")
        for func in kernel.plugins[plugin]:
            print(f"  - {func}")
    #function = kernel.get_function("genie", "start_conversation")
    result = await kernel.invoke( 
        #function,
        plugin_name="genie",
        function_name="start_conversation",
        arguments=KernelArguments({
            "space_id": request.space_id,
            "message": request.message
        })
    )

    return {
        "result": str(result)
    }
"""