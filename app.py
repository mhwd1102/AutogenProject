import agents
import chainlit as cl
from agent_profile import *

@cl.on_chat_start
async def on_chat_start():
    try:
        await cl.make_async(User_Proxy.initiate_chat)(Assistant, problem='مرحبا')
        
    except Exception as e:
        print(e)
        pass



@cl.on_message
async def on_message(message: cl.Message):
    

    task = message.content

    await cl.make_async(User_Proxy.send)(Assistant, message=task)
    

    # groupChat = agents.makeGroupChat(agents=[hrAssistant, userProxy, hrPlanner,], max_round=20,)
    # manager = agents.makeManager(groupchat=groupChat,)

    # print("GC messages: ", len(groupChat.messages))

    # if len(groupChat.messages) == 0:
    #     # await cl.Message(content=f'Starting agents on task: {task}...').send()
    #     await cl.make_async(userProxy.initiate_chat)(manager, message=task)
    # else:
    #     await cl.make_async(userProxy.send)(manager, message=task)


