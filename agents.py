from typing import List, Dict, Union, Optional
import autogen
import chainlit as cl
from autogen import Agent, AssistantAgent, UserProxyAgent, GroupChat
from functions import function_map


config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")

llm_config = {
    "config_list": config_list,
    "seed": 42, 
    "request_timeout": 120,
    "temperature": 0
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
    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ) -> bool:
        cl.run_sync(
            cl.Message(
                content=f'*Sending message to "{recipient.name}":*\n\n{message}',
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
        if prompt.startswith(
            "Provide feedback to chat_manager. Press enter to skip and use auto-reply"
        ):
            res = cl.run_sync(
                ask_helper(
                    cl.AskActionMessage,
                    content="Continue or provide feedback?",
                    actions=[
                        cl.Action( name="continue", value="continue", label="✅ Continue" ),
                        cl.Action( name="feedback",value="feedback", label="💬 Provide feedback"),
                        cl.Action( name="exit",value="exit", label="🔚 Exit Conversation" )
                    ],
                )
            )
            if res.get("value") == "continue":
                return ""
            if res.get("value") == "exit":
                return "exit"

        reply = cl.run_sync(ask_helper(cl.AskUserMessage, content=prompt, timeout=60))

        return reply["content"].strip()

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        cl.run_sync(
            cl.Message(
                content=f'*Sending message to "{recipient.name}"*:\n\n{message}',
                author=self.name,
            ).send()
        )
        super(ChainlitUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )

def makeAssistantAgent(name: str, system_message: str):
    return ChainlitAssistantAgent(
        name=name,
        llm_config=llm_config,
        system_message=system_message
    )

def makeAdminAgent(name: str, system_message: str):
    return ChainlitUserProxyAgent(
        name=name,
        llm_config=llm_config,
        system_message=system_message,
        code_execution_config={
            "work_dir": "HR",
            "use_docker": False,
        },
        human_input_mode="NEVER"
    )

def makeUserProxyAgent(name: str, system_message: str, human_input_mode: str, max_consecutive_auto_reply: int):
    if human_input_mode != "TERMINATE":
        return ChainlitUserProxyAgent(
        name=name,
        system_message=system_message,
        human_input_mode=human_input_mode,
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        llm_config=llm_config,
        function_map=function_map,
        )
    is_termination_msg = lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
    return ChainlitUserProxyAgent(
        name=name,
        system_message=system_message,
        human_input_mode=human_input_mode,
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        is_termination_msg=is_termination_msg,
        llm_config=llm_config,
        function_map=function_map,
    )

def makeGroupChat(agents: List[Agent], max_round: int):
    return autogen.GroupChat(
        agents=agents,
        messages=[],
        max_round=max_round
    )

def makeManager(groupchat: GroupChat):
    return autogen.GroupChatManager(
        groupchat=groupchat
    )
    
    