import agents
import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    try:
        # hrSystem = agents.makeAdminAgent(
        #     name="HR_System",
        #     system_message="""
        #     You execute the code given to you and return the result.
        #     Any input in the code ask the HR Admin for it.
        #     """
        # )
        # hrAdmin = agents.makeAdminAgent(
        #     name="HR_Admin",
        #     system_message="""
        #     You are the an HR admin that responds to the approved HR request and update the system accordingly. 
        #     Any information You need you ask the HR Assitant for it. You always update the HR Assistant about your progress. 
        #     Give the HR System code to update the json file (dummydata.json) with the new information.
        #     You do not Comunicate with the User Proxy.
        #     """
        # )
        hrAssistant = agents.makeAssistantAgent(
            name="HR_Assistant",
            system_message="""
            You are an HR assistant. 
            You are the middle man between the User Proxy and the HR Manager.
            Check if the Employee id is valid using validate_employee_id.
            if the Employee id is valid send the request to the HR manager and provide the User Proxy with request number.
            if the Employee id is not valid, ask the user for a vaild Employee id.
            If the request is approved you send the request to the HR Admin to make the changes in the system.
            Then the you send the result to the User proxy.
            """,
        )
        hrManager = agents.makeAssistantAgent(
            name="HR_Manager",
            system_message="""
            You are the manager of the HR department. You approve or reject the HR requests. 
            You can also ask for more information from the HR Assistant. 
            If the request is rejected, you can ask for more information from HR Assistant. 
            Check if the employee has enough vacation days using get_vacation_balance.
            if the employee has vacation balance less than the requested days, you reject the request.
            if the employee has enough vacation days, you approve the request.
            provide the HR assistant with the reason for approval or rejection.
            after two tries if the information is not sufficient, you can reject the request and give it back to HR Assistant. 
            if approved you send it back to the HR Assistant. 
            You do not Comunicate with the User Proxy.
            """
        )
        userProxy = agents.makeUserProxyAgent(
            name="User_Proxy",
            system_message="""
            You are a user that sends HR requests to the HR Assistant. 
            when asked for more information you wait for user input and send it bact to the HR assistant.
            """,
            human_input_mode="ALWAYS",
            max_consecutive_auto_reply=1,
        )

        # cl.user_session.set("HR_Admin", hrAdmin)
        cl.user_session.set("HR_Assistant", hrAssistant)
        cl.user_session.set("HR_Manager", hrManager)
        cl.user_session.set("User_Proxy", userProxy)
        # cl.user_session.set("HR_System", hrSystem)

        await cl.Message(content="Welcome to the company! I am your HR assistant. How can I help you?", author="HR Assistant").send()
    except Exception as e:
        print(e)
        pass

@cl.on_message
async def on_message(message: cl.Message):
    
    try:
        task = message.content
        # print(f'User: {task}')
        # hrAdmin = cl.user_session.get("HR_Admin")
        hrProxy = cl.user_session.get("HR_Assistant")
        hrManager = cl.user_session.get("HR_Manager")
        userProxy = cl.user_session.get("User_Proxy")
        # hrSystem = cl.user_session.get("HR_System")

        groupChat = agents.makeGroupChat(agents=[hrProxy, hrManager, userProxy], max_round=20)
        manager = agents.makeManager(groupchat=groupChat)

        print("GC messages: ", len(groupChat.messages))

        if len(groupChat.messages) == 0:
            # await cl.Message(content=f'Starting agents on task: {task}...').send()
            await cl.make_async(userProxy.initiate_chat)(manager, message=task)
        else:
            await cl.make_async(userProxy.send)(manager, message=task)

    except Exception as e:
        print(e)
        pass

