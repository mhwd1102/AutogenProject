from typing import List, Dict, Union, Optional
import autogen
import chainlit as cl
from autogen import Agent, AssistantAgent, UserProxyAgent, GroupChat
from functions import function_map, functions

config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")

llm_config = {
    "config_list": config_list,
    "seed": 42, 
    "request_timeout": 60,
    "temperature": 0,
    "functions": functions,
}


async def ask_helper(func, **kwargs):
    res = await func(**kwargs).send()
    while not res:
        res = await func(**kwargs).send()
    return res

class ChainlitAssistantAgent(AssistantAgent):
    """
    Wrapper for AutoGens Assistant Agent
    """
    flag = False

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ) -> bool:
        if self.flag:
            return True, "TERMINATE"
        if isinstance(message, str) and message.endswith("TERMINATE"):
            new_msg = message.replace("TERMINATE", "")
            cl.run_sync(  
                cl.Message(
                    content=new_msg,
                    author=self.name,
                ).send()
            )
            cl.run_sync(
                cl.Message(
                    content="Chat session has ended, Start a new chat if you have another request.",
                    author='System',
                ).send()
            )
            super(ChainlitAssistantAgent, self).send(
                message=message,
                recipient=recipient,
                request_reply=False,
                silent=silent,
            )
            self.flag = True
            return True, "TERMINATE"
        if isinstance(message, dict) and isinstance(message['content'], str) and message["content"].endswith("TERMINATE"):
            new_msg = message["content"].replace("TERMINATE", "")
            cl.run_sync(  
                cl.Message(
                    content=new_msg,
                    author=self.name,
                ).send()
            )
            cl.run_sync(
                cl.Message(
                    content="Chat session has ended, Start a new chat if you have another request.",
                    author='System',
                ).send()
            )
            super(ChainlitAssistantAgent, self).send(
                message=message["content"],
                recipient=recipient,
                request_reply=False,
                silent=silent,
            )
            self.flag = True
            return True, "TERMINATE"
        if self.name == "HR_Assistant" and isinstance(message, str):
            cl.run_sync(  
                cl.Message(
                    content=message,
                    author=self.name,
                ).send()
            )
        super(ChainlitAssistantAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )

class ChainlitUserProxyAgent(UserProxyAgent):
    """
    Wrapper for AutoGens UserProxy Agent. Simplifies the UI by adding CL Actions. 
    """
    def get_human_input(self, prompt: str) -> str:
        if self.last_message()["content"].endswith("TERMINATE"):
            print("TERMINATE")
            return 'exit'
        if prompt.startswith(
            "Provide feedback to chat_manager. Press enter to skip and use auto-reply"
        ):
            reply = cl.run_sync(ask_helper(cl.AskUserMessage, content="Please Provide an answer", timeout=60))

            return reply["content"].strip()
            

        # res = cl.run_sync(
        #     ask_helper(
        #         cl.AskActionMessage,
        #         content="Continue or provide feedback?",
        #         actions=[
        #             cl.Action(name="I want a Vacation", value="I want a Vacation", label="I want a Vacation" ),
        #             cl.Action(name="I don't feel well",value="I don't feel well", label="I don't feel well"),
        #             cl.Action(name="I want a raise",value="I want a raise", label="I want a raise" ),
        #             cl.Action(name="I want a Document", value="I want a Document"),
        #         ],
        #     )
        # )
        # if res.get("value") == "I want a Vacation":
        #     return "I want a Vacation"
        # elif res.get("value") == "I don't feel well":
        #     return "I don't feel well"
        # elif res.get("value") == "I want a raise":
        #     return "I want a raise"
        # elif res.get("value") == "I want a Document":
        #     return "I want a Document"

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        # cl.run_sync(
        #     cl.Message(
        #         content=f'*Sending message to "{recipient.name}"*:\n\n{message}',
        #         author=self.name,
        #     ).send()
        # )
        super(ChainlitUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )

        

def makeAssistantAgent(name: str, system_message: str):
    return ChainlitAssistantAgent(
        name=name,
        llm_config= llm_config,
        system_message=system_message,
        human_input_mode="NEVER"
    )

def makeAdminAssistantAgent(name: str, system_message: str):
    return ChainlitAssistantAgent(
        name=name,
        llm_config= llm_config,
        system_message=system_message,
        function_map=function_map,
        human_input_mode="NEVER"
    )

def makeUserProxyAgent(name: str, human_input_mode: str, max_consecutive_auto_reply: int):
    if human_input_mode != "TERMINATE":
        return ChainlitUserProxyAgent(
        name=name,
        human_input_mode=human_input_mode,
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        )
    is_termination_msg = lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
    return ChainlitUserProxyAgent(
        name=name,
        human_input_mode=human_input_mode,
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        is_termination_msg=is_termination_msg,
    )

def makeGroupChat(agents: List[Agent], max_round: int, messages: List[str] = []):
    return autogen.GroupChat(
        agents=agents,
        messages=messages,
        max_round=max_round
    )

def makeManager(groupchat: GroupChat):
    return autogen.GroupChatManager(
        groupchat=groupchat,
    )
    
    