import json

def give_vacation(employee_id, vacation_days):
    with open('dummydata.json', 'r+') as f:
        data = json.load(f)
        for i in data:
            if i['employee_id'] == employee_id:
                i['vacation_balance'] -= vacation_days
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                return f'Vacation balance updated successfully. Your new vacation balance is {i["vacation_balance"]}'

def get_vacation_balance(employee_id):
    with open('dummydata.json', 'r') as f:
        data = json.load(f)
        for i in data:
            if i['employee_id'] == employee_id:
                return f'Your vacation balance is {i["vacation_balance"]}'
    return "Invalid employee id, please try again."

def validate_employee_id(employee_id):
    with open('dummydata.json', 'r') as f:
        data = json.load(f)
        for i in data:
            if i['employee_id'] == employee_id:
                return "Valid employee id."
    return "Invalid employee id, please try again."

def get_work_flow(code):
    if code == "CA9001":
        return """
        This is the work flow for asking for Vacation request (code: CA9001):
        1. HR Assistant receives the request and asks for the employee id if not givin.
        2. HR Assistant sends the employee id to the HR Admin to check if it is valid using function validate_employee_id.
        3. HR Admin sends the result to the HR Assistant.
        3.1. If the employee id is not valid, HR Assistant asks the User Proxy for a valid employee id and go back to step 2.
        3.2. If the employee id is valid, HR Assistant asks the User Proxy for the number of vacation days if not givin.
        4. HR Assistant sends the number of vacation days to the HR Admin to check if the employee has enough vacation days using function get_vacation_balance.
        4.1. If the employee does not have enough vacation days, HR Assistant tells the User proxy the employees balance and asks to change the its vacation days.
        4.2. If the employee has enough vacation days, HR Assistant sends the request to the HR Manager to approve it.
        5. HR Manager approve the request only if the empolyee has enough balance.
        6. HR Assistant sends the result to the HR Admin to change the balance in the system using function give_vacation.
        7. HR Admin sends the result to the HR Assistant if it is done or not.
        8. HR Assistant sends the result to the User Proxy.
        """
    elif code == "CA9002":
        return """
        This is the work flow for asking for Sick leave request (code: CA9002):
        1. HR Assistant receives the request and asks for the employee id if not givin.
        2. HR Assistant sends the employee id to the HR Admin to check if it is valid using function validate_employee_id.
        3. HR Admin sends the result to the HR Assistant.
        3.1. If the employee id is not valid, HR Assistant asks the User Proxy for a valid employee id and go back to step 2.
        3.2. If the employee id is valid, HR Assistant send the request to the HR Manager to approve it.
        4. HR Manager approve the request.
        5. HR Assistant sends the approved request to the User Proxy and wish to get well soon.
        """
    elif code == "CA9003":
        return """
        This is the work flow for asking for Raise in salary request (code: CA9003):
        1. HR Assistant receives the request and asks for the employee id if not givin.
        2. HR Assistant sends the employee id to the HR Admin to check if it is valid using function validate_employee_id.
        3. HR Admin sends the result to the HR Assistant.
        3.1. If the employee id is not valid, HR Assistant asks the User Proxy for a valid employee id and go back to step 2.
        3.2. If the employee id is valid, HR Assistant sends to the User Proxy the employee's salary has increased by 200.
        """
    elif code == "CA9004":
        return """
        This is the work flow for asking for Document request (code: CA9004):
        1. HR Assistant receives the request and asks for the employee id if not givin.
        2. HR Assistant sends the employee id to the HR Admin to check if it is valid using function validate_employee_id.
        3. HR Admin sends the result to the HR Assistant.
        3.1. If the employee id is not valid, HR Assistant asks the User Proxy for a valid employee id and go back to step 2.
        3.2. If the employee id is valid, HR Assistant tells the User Proxy that the document will be sent via email.
        """

give_vacation_func = {
    "name": "give_vacation",
    "description": "This function is userful to give vacation to an employee.",
    "parameters": {
        "type": "object",
        "properties": {
            "employee_id": {
                "type": "integer",
                "description": "the employee id is a number with 4 digits.",
            },
            "vacation_days": {
                "type": "integer",
                "description": "The positive number of vacation days.",
            },
        },
    },
}

get_vacation_balance_func = {
    "name": "get_vacation_balance",
    "description": "This function is userful to get the vacation balance of an employee.",
    "parameters": {
        "type": "object",
        "properties": {
            "employee_id": {
                "type": "integer",
                "description": "the employee id is a number with 4 digits.",
            },
        },
        "required": ["employee_id"],
    },
}   

validate_employee_id_func = {
    "name": "validate_employee_id",
    "description": "This function is userful to check if the employee id is valid.",
    "parameters": {
        "type": "object",
        "properties": {
            "employee_id": {
                "type": "integer",
                "description": "the employee id is a number with 4 digits.",
            },
        },
        "required": ["employee_id"],
    },
}

get_work_flow_func ={
    "name": "get_work_flow",
    "description": "This function is userful to get the work flow of a request.",
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "the code of the request.",
            },
        },
        "required": ["code"],
    },
}

functions = [get_vacation_balance_func, validate_employee_id_func, give_vacation_func, get_work_flow_func,]

function_map = {
    "get_vacation_balance": get_vacation_balance,
    "validate_employee_id": validate_employee_id,
    "give_vacation": give_vacation,
    "get_work_flow": get_work_flow,
}
