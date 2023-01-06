import sys
import io
# Import load to load data
import utils.load as load
# Import helper
from utils.helperModules import getTimeStamp
# Use to print utf-8 encoded
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#----- Declare init variables  -----#

# Start time of each Task
startTime = dict()

# End time of each Task
endTime = dict()

# Start time of each Order
startTimeOrders = dict()

# End time of each Order
endTimeOrders = dict()

# Endtime using resource (employee, machine)
endTimeResource = dict()

# Average skil of each employee
avgSkill = dict()

# Base salary of each employee (per hour)
baseSalary = dict()

# Employee assign for tasks
e = dict()

# Machine assign for tasks
m = dict()

#------- Load raw data from json data ---------#
ORDERS = load.data["bills"]  # List of orders
TASKS = load.data["fromStockJobTasks"]    # List of tasks
EMPLOYEES = load.data["fromStockHumanResources"]    # List of employees
MACHINES = load.data["fromStockMachineResources"]   # List of machines

#---------- Calculate init data ------------#
# Init Start time and End time of each task 
for order in ORDERS :
    orderId = order['id']
    startTime[orderId] = dict()
    endTime[orderId] = dict()
    for item in order["goods"]:
        processId = item['goodId']
        endTime[orderId][processId] = dict()
        startTime[orderId][processId] = dict()
        for task in TASKS:
            taskId = task['id']
            startTime[orderId][processId][taskId] = getTimeStamp(order["startTime"])
            endTime[orderId][processId][taskId] = getTimeStamp(order["startTime"])

# Init avgSkill of each Task each employee
for employee in EMPLOYEES:
    avgSkill[employee['id']] = dict()
    for task in TASKS:
        avg = 0
        sumSkillValue = 0
        sumSkill = 0
        for skill in task["skills"]:
            sumSkillValue += employee["skillLevel"][skill]
            sumSkill += 1
        if(sumSkill != 0):   avg = sumSkillValue / sumSkill
        avgSkill[employee['id']][task['id']] = avg
    

# Init base Salary of employees:
for employee in EMPLOYEES:
    employeeId = employee['id']
    baseSalary[employeeId] = employee['cost']

# Init endTime and startTime of orders:
for order in ORDERS:
    endTimeOrders[order['id']] = getTimeStamp(order['deadline'])
    startTimeOrders[order['id']] = getTimeStamp(order['startTime'])

# Init list employee Id
listEmployeeIds = list()
for emp in EMPLOYEES:
    listEmployeeIds.append(emp['id'])
        