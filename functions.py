import json

def decrease_vacation_days(employee_id, vacation_days):
    with open('dummydata.json', 'r+') as f:
        data = json.load(f)
        for i in data:
            if i['employee_id'] == employee_id and i['vacation_balance'] >= vacation_days:
                i['vacation_balance'] -= vacation_days
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                return f'Vacation balance updated successfully. Your new vacation balance is {i["vacation_balance"]}'
            elif i['employee_id'] == employee_id and i['vacation_balance'] < vacation_days:
                return f'Insufficient vacation balance. Your current vacation balance is {i["vacation_balance"]}'
    return "Invalid employee id, please try again."

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

def get_employee_salary(employee_id):
    with open('dummydata.json', 'r') as f:
        data = json.load(f)
        for i in data:
            if i['employee_id'] == employee_id:
                return f'The salary is {i["salary"]}'
    return "Invalid employee id, please try again."

def increase_salary(employee_id):
    with open('dummydata.json', 'r+') as f:
        data = json.load(f)
        for i in data:
            if i['employee_id'] == employee_id and i['salary'] < 10000:
                i['salary'] += 2000
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                return f'Your new salary is {i["salary"]}'
            elif i['employee_id'] == employee_id and i['salary'] >= 10000:
                return f'Your salary is already above $10,000. Your current salary is {i["salary"]}'
    return "Invalid employee id, please try again."


def get_work_flow(code):
    if code == "CA9001":
        return """
        For Vacation Request (code: CA9001):
        1. HR Assistant receives the request and prompts for the employee ID if not provided.
        2. HR Assistant forwards the employee ID to the HR Planner to validate using 'validate_employee_id' function.
        3. HR Planner communicates the validation result back to the HR Assistant.
        3.1. If the employee ID is invalid, HR Assistant requests a valid one from the User Proxy and returns to step 2.
        3.2. If the employee ID is valid, HR Assistant asks the User Proxy for the number of vacation days if not provided.
        4. HR Assistant verifies the employee's vacation balance by sending the number of vacation days to the HR Planner using 'get_vacation_balance' function.
        4.1. If the employee lacks sufficient vacation days, HR Assistant informs the User Proxy of the balance and requests a modification of the vacation days.
        4.2. If enough vacation days are available, HR Assistant forwards the request to the HR Planner to adjust the balance in the system using 'decrease_vacation_days' function.
        5. HR Planner communicates the outcome (whether completed or not) back to the HR Assistant.
        6. HR Assistant relays the result to the User Proxy.
        """
    elif code == "CA9002":
        return """
        For Sick Leave Request (code: CA9002):
        1. HR Assistant receives the request and prompts for the employee ID if not provided.
        2. HR Assistant forwards the employee ID to the HR Planner to validate using 'validate_employee_id' function.
        3. HR Planner communicates the validation result back to the HR Assistant.
        3.1. If the employee ID is invalid, HR Assistant requests a valid one from the User Proxy and returns to step 2.
        3.2. If the employee ID is valid, HR Assistant approves the request and extends wishes for a speedy recovery.
        """
    elif code == "CA9003":
        return """
        For Raise in Salary Request (code: CA9003):
        1.HR Assistant receives the request and prompts for the employee ID if not provided.
        2.HR Assistant forwards the employee ID to the HR Planner to validate using 'validate_employee_id' function.
        3.HR Planner communicates the validation result back to the HR Assistant.
        3.1. If the employee ID is invalid, HR Assistant requests a valid one from the User Proxy and returns to step 2.
        3.2. If the employee ID is valid, check the salary of the employee using 'get_employee_salary' function.
        4. If the salary is less than $10,000, HR Assistant forwards the request to the HR Planner to adjust the salary in the system using 'increase_salary' function.
        5. HR Planner communicates the outcome (whether completed or not) back to the HR Assistant.
        6. HR Assistant relays the result to the User Proxy.
        """
    elif code == "CA9004":
        return """
        For Document Request (code: CA9004):
        1. HR Assistant receives the request and prompts for the employee ID if not provided.
        2. HR Assistant forwards the employee ID to the HR Planner to validate using 'validate_employee_id' function.
        3. HR Planner communicates the validation result back to the HR Assistant.
        3.1. If the employee ID is invalid, HR Assistant requests a valid one from the User Proxy and returns to step 2.
        3.2. If the employee ID is valid, HR Assistant informs the User Proxy that the document will be sent via email.
        """
    else:
        return "Invalid code, please try again."

decrease_vacation_days_func = {
    "name": "decrease_vacation_days",
    "description": "This function is userful to give vacation to an employee.",
    "parameters": {
        "type": "object",
        "properties": {
            "employee_id": {
                "type": "string",
                "description": "the employee with the format 'EMP****'.",
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
                "type": "string",
                "description": "the employee id with the format 'EMP****'.",
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
                "type": "string",
                "description": "the employee id with the format 'EMP****'.",
            },
        },
        "required": ["employee_id"],
    },
}

get_employee_salary_func = {
    "name": "get_employee_salary",
    "description": "This function is userful to get the salary of an employee.",
    "parameters": {
        "type": "object",
        "properties": {
            "employee_id": {
                "type": "string",
                "description": "the employee id with the format 'EMP****'.",
            },
        },
        "required": ["employee_id"],
    },
}

increase_salary_func = {
    "name": "increase_salary",
    "description": "This function is userful to increase the salary of an employee.",
    "parameters": {
        "type": "object",
        "properties": {
            "employee_id": {
                "type": "string",
                "description": "the employee id with the format 'EMP****'.",
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
                "description": "the code of the request following this format CA9***.",
            },
        },
        "required": ["code"],
    },
}

functions = [get_vacation_balance_func, validate_employee_id_func, decrease_vacation_days_func, get_work_flow_func, get_employee_salary_func, increase_salary_func]

function_map = {
    "get_vacation_balance": get_vacation_balance,
    "validate_employee_id": validate_employee_id,
    "decrease_vacation_days": decrease_vacation_days,
    "get_work_flow": get_work_flow,
    "get_employee_salary": get_employee_salary,
    "increase_salary": increase_salary,
}
