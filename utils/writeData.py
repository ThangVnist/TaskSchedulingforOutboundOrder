# Python program to read
import json
import os
import copy
from datetime import datetime
from utils.helperModules import getDateTimeFromTimestamp
from utils.initializeData import listEmployeeIds, MACHINES


# Get dir to data ouput folder
def getAbsoluteDirectory(pathFile):
    script_dir = os.path.dirname(__file__)
    rel_path = pathFile
    project_dir = script_dir.split("utils")[0]
    return os.path.join(project_dir, rel_path)


def formatDateTimeSchedules(schedules):
    # Format date time
    for schedule in schedules:
        #sort task by startTime
        schedule['schedule'].sort(key=lambda x:x['startTime'])

        for task in schedule['schedule']:
            task['startTime'] = getDateTimeFromTimestamp(task['startTime']).strftime("%d/%m/%Y, %H:%M")
            task['endTime'] = getDateTimeFromTimestamp(task['endTime']).strftime("%d/%m/%Y, %H:%M")
        schedule['endDateTime'] = getDateTimeFromTimestamp(schedule['endDateTime']).strftime("%d/%m/%Y, %H:%M")
        schedule['startDateTime'] = getDateTimeFromTimestamp(schedule['startDateTime']).strftime("%d/%m/%Y, %H:%M")


# Write data output for tasks
def writeOutputForTasks(schedules):
    # Write file
    with open("result.json", "w") as outfile:
        json.dump(schedules, outfile, indent=2, separators=(',', ': '))

    # Save as history file
    now = datetime.now()  # current date and time
    date_time = now.strftime("%d_%m_%Y_%H-%M-%S")
    rel_path = f"data/output/Result_{date_time}.json"
    with open(getAbsoluteDirectory(rel_path), "w") as outfile:
        json.dump(schedules, outfile, indent=2, separators=(',', ': '))


# Write data output for employees
def writeOutputForEmployees(schedules):
    listSchedule = schedules.copy()

    for schedule in listSchedule:
        employees = {}

        for employeeId in listEmployeeIds:
            employees[employeeId] = []

        for task in schedule['schedule']:
            employees[task['employeeId']].append(task)
        schedule['schedule'] = employees

    # Write file
    with open("result_employees.json", "w") as outfile:
        json.dump(listSchedule, outfile, indent=2, separators=(',', ': '))


# Write data output for machines
def writeOutputForMachines(schedules):
    listSchedule = schedules.copy()

    for schedule in listSchedule:
        machines = {}

        for machine in MACHINES:
            machines[machine['id']] = []
        machines['null'] = []

        for task in schedule['schedule']:
            machines[task['machineId']].append(task)
        schedule['schedule'] = machines

    # Write file
    with open("result_machines.json", "w") as outfile:
        json.dump(listSchedule, outfile, indent=2, separators=(',', ': '))


# Write data output
def writeOutput(schedules):
    formatDateTimeSchedules(schedules)

    writeOutputForTasks(copy.deepcopy(schedules))
    writeOutputForEmployees(copy.deepcopy(schedules))
    writeOutputForMachines(copy.deepcopy(schedules))
