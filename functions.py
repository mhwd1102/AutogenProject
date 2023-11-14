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

give_vacation_func = {
    "name": "give_vacation",
    "description": "This function is userful to give vacation to an employee.",
    "parameters": {
        "type": "object",
        "properties": {
            "employee_id": {
                "type": "integer",
                "description": "the employee id is a numeric string with 4 digits.",
            },
            "vacation_days": {
                "type": "integer",
                "description": "the number of vacation days.",
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
                "description": "the employee id is a numeric string with 4 digits.",
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
                "description": "the employee id is a numeric string with 4 digits.",
            },
        },
        "required": ["employee_id"],
    },
}

functions = [get_vacation_balance_func, validate_employee_id_func, give_vacation_func]

function_map = {
    "get_vacation_balance": get_vacation_balance,
    "validate_employee_id": validate_employee_id,
    "give_vacation": give_vacation,
}
