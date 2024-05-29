from enum import Enum
from typing import Annotated, List, Literal, Optional
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


PyObjectId = Annotated[str, BeforeValidator(str)]

class Agent_Type(str, Enum):
    TOOL_CALLING = 'tool_calling'
    STRCUTURED = 'structured',  
    REACT   = 'react',
    JSON = 'json'

class Source_Type(str, Enum):
    UI = 'ui'
    CODE = 'code', 


class AgentModel(BaseModel):
    """
    Container for a single agent record.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    agent_type: str = Literal[Agent_Type.TOOL_CALLING,Agent_Type.STRCUTURED,Agent_Type.REACT,Agent_Type.JSON]
    source_type: str= Literal[Source_Type.UI,Source_Type.CODE]
    preamble: str =  Field(...)
    tools: List[str]
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class AgentsCollection(BaseModel):
    """
    A container holding a list of `AgentModel` instances.
    """

    students: List[AgentModel]