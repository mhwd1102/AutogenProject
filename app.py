import agents
import chainlit as cl
from agent_profile import *

@cl.on_chat_start
async def on_chat_start():
    try:
        cl.user_session.set("HR_Admin", HR_ADMIN)
        cl.user_session.set("HR_Assistant", HR_ASSISTANT)
        cl.user_session.set("HR_Manager", HR_MANAGER)
        cl.user_session.set("User_Proxy", USER_PROXY)

        await cl.Message(content="Welcome to the company! I am your HR assistant. How can I help you?", author="HR_Assistant").send()
    except Exception as e:
        print(e)
        pass

@cl.on_message
async def on_message(message: cl.Message):
    
    try:
        task = message.content
        # print(f'User: {task}')
        hrAdmin = cl.user_session.get("HR_Admin")
        hrAssistant = cl.user_session.get("HR_Assistant")
        hrManager = cl.user_session.get("HR_Manager")
        userProxy = cl.user_session.get("User_Proxy")
        # hrSystem = cl.user_session.get("HR_System")

        groupChat = agents.makeGroupChat(agents=[hrAssistant, hrManager, userProxy, hrAdmin], max_round=20,)
        manager = agents.makeManager(groupchat=groupChat)

        print("GC messages: ", len(groupChat.messages))

        if len(groupChat.messages) == 0:
            # await cl.Message(content=f'Starting agents on task: {task}...').send()
            await cl.make_async(userProxy.initiate_chat)(manager, message=task)
        else:
            if message.author == "HR_Assistant":
                await cl.make_async(userProxy.send)(manager, message=task)
            # await cl.make_async(userProxy.send)(manager, message=task)

    except Exception as e:
        print(e)
        pass

