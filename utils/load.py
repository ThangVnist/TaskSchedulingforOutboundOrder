# Python program to read
# json file

from datetime import datetime
from email.policy import strict
import json
from config.configData import INPUT

# Opening JSON file
f = open(INPUT, "r", encoding='utf-8')
# f = open('result.json', "r",encoding='utf-8' )

# Load data
data = json.load(f, strict=False)


# Closing file
f.close()

# schedules = data['schedule']
# totalTime = dict()
# for schedule in schedules :
#     empId = schedule['employeeId']
#     startDate = datetime.strptime(schedule['startTime'], '%d/%m/%Y, %H:%M')
#     endDate = datetime.strptime(schedule['endTime'], '%d/%m/%Y, %H:%M')
#     if empId not in totalTime.keys() : totalTime[empId] = 0
#     totalTime[empId] += (endDate.timestamp() - startDate.timestamp())/60


# # schedules = data[2]['jobTasks']
# # totalTime = dict()
# # for schedule in schedules :
# #     empId = schedule['assignedEmployeeId']
# #     startDate = datetime.strptime(schedule['startTime'], '%d-%m-%Y %H:%M %p')
# #     endDate = datetime.strptime(schedule['endTime'], '%d-%m-%Y %H:%M %p')
# #     if empId not in totalTime.keys() : totalTime[empId] = 0
# #     totalTime[empId] += (endDate.timestamp() - startDate.timestamp())/60

# print(totalTime)

# salary = {
#     '62b1a3ac29da55a4b049ae53' : 27250,
#     '62b1a3ac29da55a4b049ae65' : 24750,
#     '62b1a3ac29da55a4b049ae43' : 27750,
#     '62b1a3a691dbfba478012934' : 33000,
#     '62b1a3ac29da55a4b049ae4a' : 25250,
#     '62b1a3ac29da55a4b049ae5c' : 26250,
#     '62b1a3ac29da55a4b049ae6e' : 25750
# }
# # time = [469,	549,	523,	269,	640,	541,	376
# # ]
# maxTime = 1904
# total = 0
# for empId in salary:
#     total += salary[empId] * (maxTime - totalTime[empId])/60
# print(total)
