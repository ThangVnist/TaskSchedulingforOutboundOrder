#------- Helper method  ----------#
NUM_OBJECTIVES = 3
OBJECTIVES_WEIGHT = [1, 1, 1]

from datetime import datetime, timedelta

# Convert a String time to timestamp
def getTimeStamp(stringTime):
    formatDatetime = '%d-%m-%Y %H:%M'
    if ("AM" in stringTime ) or ("PM" in stringTime) :
        formatDatetime =  '%d-%m-%Y %H:%M %p'
    res = datetime.strptime(stringTime, formatDatetime)
    return res.timestamp()

# Calculate duration task time in practical from employee and skill level
def calculateDuration(task, avgSkill, employeeId):
    oldDuration = task["estimatedDuration"] * 3600
    taskId = task["id"]
    listEmpId = avgSkill.keys()
    totalSkillLevel = 0
    for empId in listEmpId :
        totalSkillLevel += avgSkill[f"{empId}"][taskId]
    avgSkillLevel = totalSkillLevel / len(listEmpId)

    newDuration = oldDuration * (1 - (avgSkill[employeeId][taskId] - avgSkillLevel) / avgSkillLevel)
    return newDuration

# Calculate the start time in practical if it violated shift time
def getStartTimeShift(startTime, duration):
    startDateTime = datetime.fromtimestamp(startTime)
    endDateTime = datetime.fromtimestamp(startTime + duration)
    nextDay = startDateTime + timedelta(days=1)
    today12h = datetime(startDateTime.year, startDateTime.month, startDateTime.day, 12, 0 ,0).timestamp()
    today13h = datetime(startDateTime.year, startDateTime.month, startDateTime.day, 13, 0 ,0).timestamp()
    startHour, endHour = startDateTime.hour, endDateTime.hour
    startMinute, endMinute = startDateTime.minute, endDateTime.minute

    if(startHour > 17 or (startHour == 17 and startMinute > 30) or endHour > 17 or (endHour == 17 and endMinute > 30)):    
        startDateTime = datetime(nextDay.year, nextDay.month, nextDay.day, 8, 0, 0)
    
    if(startTime < today12h and ((startTime + duration > today12h))):    
        return today13h
    return startDateTime.timestamp()

def getDateTimeFromTimestamp(timestamp):
    res = datetime.fromtimestamp(timestamp)
    return res

# Calculate cost of each employee with duration
def getCost(employeeId, duration, baseSalary):
    return baseSalary[employeeId] * duration / 3600

# Calculate score for solutions and get best solution.
def getBestSolution(objectives, solutions) :
    maxObjectives, minObjectives , rangeObjectives, bestSolution = list(),  list(), list(), list()
    score = 999999999
    for i in range(0, NUM_OBJECTIVES):
        maxObjectives.append(0)
        minObjectives.append(9999999999999999)
        rangeObjectives.append(0)

    for objective in objectives:
        for i in range(0, NUM_OBJECTIVES):
            maxObjectives[i] = max(maxObjectives[i], objective[i])
            minObjectives[i] = min(minObjectives[i], objective[i])
            
            
    
    for i in range(0, NUM_OBJECTIVES):
        rangeObjectives[i] = maxObjectives[i] - minObjectives[i]
        if(rangeObjectives[i] == 0) : rangeObjectives[i] = 1
    
    for j in range(0, len(objectives)):
        obj_score = 0
        for i in range(0, NUM_OBJECTIVES):
            obj_score += (objectives[j][i] - minObjectives[i]) / rangeObjectives[i] * OBJECTIVES_WEIGHT[i]
        if( obj_score < score):
            score = obj_score
            bestSolution.append(solutions[j])

    return bestSolution
#test
# task = {
#       "id": "j1",
#       "code": "DXT_b06305c0-f150-11ec-9cb9-e72d112caadc",
#       "requiredAssets": [
#       ],
#       "skills": [
#         "62b1a3ac29da55a4b049ae80",
#         "62b1a3ac29da55a4b049ae81",
#         "62b1a3ac29da55a4b049ae83"
#       ],
#       "group": "1",
#       "estimatedDuration": 0.1,
#       "estimateOptimisticTime": 1,
#       "estimateNormalCost": 100,
#       "estimateMaxCost": 200,
#       "estimateAssetCost": 100,
#       "followingTasks": [],
#       "priority": 1,
#       "preceedingTasks": [],
#       "name": "In tài liệu đơn hàng",
#       "taskWeight": {
#         "timeWeight": 0.3333333333333333,
#         "qualityWeight": 0.3333333333333333,
#         "costWeight": 0.3333333333333333
#       }
#     }
# avgSkill = {
#     "62b1a3a691dbfba478012934": {
#         "j1": 0.3,
#         "j2": 0.4
#     },
#     "62b1a3a691dbfba478012931": {
#         "j1": 0.1,
#         "j2": 0.2
#     }
# }
# emp = Employee("62b1a3a691dbfba478012934", 300, [])
# calculateDuration(task, avgSkill, emp)
# F = [[2.69329133e+06, 1.66027347e+09, 0.00000000e+00],
#  [2.61128124e+06, 1.66027443e+09, 0.00000000e+00],
#  [2.59230963e+06, 1.66027493e+09,0.00000000e+00],
#  [1.53467044e+06, 1.66027859e+09, 0.00000000e+00],
#  [1.55488019e+06, 1.66027831e+09, 0.00000000e+00]]

# a = getBestSolution(F)
# print(a)
