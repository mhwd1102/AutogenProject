def give_vacation(id, days):
    import json
    with open('dummydata.json', 'r+') as f:
        data = json.load(f)
        for i in data:
            if i['id'] == id:
                i['vacation'] -= days
                break
        json.dump(data, f, indent=4)
    return True

def get_vacation_balance(employee_id):
    print("get_vacation_balance is called")
    return 5

def validate_employee_id(employee_id):
    if employee_id == 1001:
        return "Employee ID is valid."
    else:
        return "Employee ID is not valid."

get_vacation_balance_func = {
        "name": "get_vacation_balance",
        "description": "This function is userful to get the vacation balance of an employee.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
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
                    "type": "string",
                    "description": "the employee id is a numeric string with 4 digits.",
                },
            },
            "required": ["employee_id"],
        },
    
}


functions = [get_vacation_balance_func, validate_employee_id_func]


function_map = {
    "get_vacation_balance": get_vacation_balance,
    "validate_employee_id": validate_employee_id,
}
