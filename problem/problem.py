from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer, Choice, Binary
from utils.helperModules import calculateDuration, getStartTimeShift, getCost, getMachineCost, getTimeStamp, getActualWorkingTime, getPenaltyFee

from utils.initializeData import startTime, baseSalary, baseMachineCost, endTime, \
    endTimeOrders, endTimeResource, listEmployeeIds, e, m, avgSkill, TASKS, MACHINES, EMPLOYEES, ORDERS, penaltyFeeOrders


class MultiObjectiveMixedVariableProblem(ElementwiseProblem):

    # Init decision variables for problem
    def __init__(self, **kwargs):

        vars = dict()
        for order in ORDERS:
            for item in order["goods"]:
                for task in TASKS:
                    vars[f"e {order['id']} {item['goodId']} {task['id']}"] = Choice(options=listEmployeeIds)
                    if task["requiredAssets"]:
                        vars[f"m {order['id']} {item['goodId']} {task['id']}"] = Choice(options=task["requiredAssets"])

        super().__init__(vars=vars, n_obj=3, **kwargs)

    # Evaluate values of fitness functions
    def _evaluate(self, X, out, *args, **kwargs):
        for order in ORDERS:
            orderId = order['id']
            e[orderId] = dict()
            m[orderId] = dict()
            for item in order["goods"]:
                processId = item['goodId']
                e[orderId][processId] = dict()
                m[orderId][processId] = dict()
                for task in TASKS:
                    taskId = task['id']
                    e[orderId][processId][taskId] = X[f"e {orderId} {processId} {taskId}"]
                    if task["requiredAssets"]:
                        m[orderId][processId][taskId] = X[f"m {orderId} {processId} {taskId}"]

        endTimeResource.clear()
        for order in ORDERS:
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
        # Get value of fitness functions
        schedule = self.calcSchedule()
        f1 = schedule['totalCost']
        #f2 = schedule['endDateTime'] - schedule['schedule'][0]['startTime']
        f2 = schedule['workingTime']
        f3 = schedule['numOrderNotOnTime']

        out["F"] = f1, f2, f3

    # Evaluate schedule
    def calcSchedule(self):
        endTimeResource.clear()
        scheduleWorkforce = dict()
        scheduleWorkforce['schedule'] = list()
        orderViolatedDeadline = list()
        actualEndTime = dict()
        totalCost = 0
        endTimeAll = 0
        machineCost = 0

        workingTimeTotal = dict()
        for employeeId in listEmployeeIds:
            workingTimeTotal[employeeId] = 0

        for task in TASKS:
            taskId = task['id']
            for order in ORDERS:
                orderId = order['id']
                actualEndTime[order['id']] = 0
                for item in order["goods"]:
                    processId = item['goodId']
                    empAssignId = e[orderId][processId][taskId]
                    if taskId in m[orderId][processId]:
                        machineAssignId = m[orderId][processId][taskId]
                    else:
                        machineAssignId = "null"
                    # Calculate duration by employee Skill
                    newDuration = calculateDuration(task, avgSkill, empAssignId)
                    workingTimeTotal[empAssignId] += newDuration

                    # Calculate Start time
                    # If task has preceedingTask
                    if (task["preceedingTasks"]):
                        for preceeding in task["preceedingTasks"]:
                            endTimePreceeding = endTime[orderId][processId][preceeding]

                            if (endTimePreceeding > startTime[orderId][processId][taskId]):
                                startTime[orderId][processId][taskId] = endTimePreceeding

                    # If human resource is not available
                    if (empAssignId in endTimeResource.keys()):
                        if (startTime[orderId][processId][taskId] < endTimeResource[empAssignId]):
                            # Start time is endTime of emp resource
                            startTime[orderId][processId][taskId] = endTimeResource[empAssignId]

                    # If machine resource is not available
                    if (machineAssignId != "null" and (machineAssignId in endTimeResource.keys())):
                        if (startTime[orderId][processId][taskId] < endTimeResource[machineAssignId]):
                            # Start time is endTime of emp resource
                            startTime[orderId][processId][taskId] = endTimeResource[machineAssignId]

                    # Calculate start time by shift time
                    startTime[orderId][processId][taskId] = getStartTimeShift(startTime[orderId][processId][taskId],
                                                                              newDuration)

                    # Calculate endtime
                    endTime[orderId][processId][taskId] = startTime[orderId][processId][taskId] + newDuration

                    actualEndTime[order['id']] = max(actualEndTime[order['id']], endTime[orderId][processId][taskId])
                    # Calculate endtime human resource and machine Resource
                    endTimeResource[empAssignId] = endTime[orderId][processId][taskId]
                    if (machineAssignId != "null" and (machineAssignId in endTimeResource.keys())):
                        endTimeResource[machineAssignId] = endTime[orderId][processId][taskId]

                    # Calculate total cost
                    totalCost += getCost(empAssignId, newDuration, baseSalary)
                    # Calculate total machine cost
                    if machineAssignId != "null":
                        machineCost += getMachineCost(machineAssignId, newDuration, baseMachineCost)
                    # Calculate endTimeAll
                    if (endTimeAll < endTime[orderId][processId][taskId]):
                        endTimeAll = endTime[orderId][processId][taskId]
                    # Calculate task not on time
                    if (endTime[orderId][processId][taskId] > endTimeOrders[orderId]):
                        if (orderId not in orderViolatedDeadline):
                            orderViolatedDeadline.append(orderId)
                    # add Task to Workforce
                    scheduleWorkforce['schedule'].append({
                        "orderId": orderId,
                        "processId": processId,
                        "taskId": taskId,
                        'employeeId': empAssignId,
                        'machineId': machineAssignId,
                        'startTime': startTime[orderId][processId][taskId],
                        'endTime': endTime[orderId][processId][taskId],
                    })

        #Calculate penalty fee for orders
        penaltyFeeTotal = 0
        for order in ORDERS:
            orderId = order['id']
            if (actualEndTime[orderId] > endTimeOrders[orderId]):
                penaltyFeeTotal += getPenaltyFee(
                    orderId,
                    getActualWorkingTime(getTimeStamp(order["startTime"]),actualEndTime[orderId]),
                    penaltyFeeOrders
                )

        salaryTotal = 0
        workingTime = getActualWorkingTime(scheduleWorkforce['schedule'][0]['startTime'], endTimeAll)
        scheduleWorkforce['employees'] = dict()
        scheduleWorkforce['employees']['value'] = dict()
        scheduleWorkforce['employees']['workingTime'] = workingTime

        # Calculate salary for employees
        for employeeId in listEmployeeIds:
            salaryTotal += getCost(employeeId, workingTime, baseSalary)

            scheduleWorkforce['employees']['value'][employeeId] = dict()
            scheduleWorkforce['employees']['value'][employeeId]['workingTime'] = workingTimeTotal[empAssignId]
            scheduleWorkforce['employees']['value'][employeeId]['ratio'] = 100 * workingTimeTotal[empAssignId] / workingTime

        scheduleWorkforce['totalCost'] = salaryTotal + machineCost + penaltyFeeTotal
        scheduleWorkforce['startDateTime'] = (scheduleWorkforce['schedule'][0]['startTime'])
        scheduleWorkforce['endDateTime'] = endTimeAll
        scheduleWorkforce['workingTime'] = workingTime
        scheduleWorkforce['numOrderNotOnTime'] = len(orderViolatedDeadline)
        return scheduleWorkforce

