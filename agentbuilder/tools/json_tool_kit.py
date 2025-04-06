from pathlib import Path
import yaml
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec


data_path= str(Path(__file__).parent)+"./../data"

with open(f"{data_path}/petstore.yaml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

json_spec = JsonSpec(dict_=data, max_value_length=4000)


json_toolkit = JsonToolkit(spec=json_spec)

json_tools=[]

for tool in json_toolkit.get_tools():
    if tool.metadata:
        tool.metadata["file_path"]= str(Path(__file__).absolute())
    else:
        tool.metadata = {"file_path": str(Path(__file__).absolute())}
    json_tools.append(tool)
