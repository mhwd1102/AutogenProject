import json

goodbye = "Thank you for using the system"

def giveVacation():
    id = int(input("Please enter Employee id: "))
    days = int(input("Please enter the amount of vacation days: "))
    with open('dummydata.json', 'r+') as f:
        data = json.load(f)
        for i in data:
            if i['id'] == id:
                i['vacation'] -= days
                break
        json.dump(data, f, indent=4)
    return True

print('       Welcome to HR System')
print('-----------------------------------')
while(True):
    print("1. Apply Vacation")
    print('-----------------------------------')
    choice = int("Please enter the number of the application [0 to Exit]")

    if choice == 0:
        print(goodbye)
        break
    elif choice == 1:
        flag = giveVacation()
        if flag:
            print("Vacation given Enjoy")
        else:
            print("Something went wrong")
        break
    else:
        print('Wrong input')



        

    