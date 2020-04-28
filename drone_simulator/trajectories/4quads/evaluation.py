import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider  # , Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D


traj = np.load(sys.path[0] + "/0/pos_traj_1.npy")
vel = np.load(sys.path[0] + "/0/vel_traj_1.npy")
agents = traj.shape[0]
timesteps = traj.shape[1]

deltaTime = 0.0508
startPoints = np.around(traj[:,0,:], 0)
endPoints = np.around(traj[:,-1,:], 2)

def loadTrajectories(delay, run):
    global traj
    global vel
    global agents
    global timesteps
    global startPoints
    global endPoints

    traj = np.load(sys.path[0] + f"/{delay}/pos_traj_{run}.npy")
    vel = np.load(sys.path[0] + f"/{delay}/vel_traj_{run}.npy")
    agents = traj.shape[0]
    timesteps = traj.shape[1]
    startPoints = np.around(traj[:,0,:], 0)
    endPoints = np.around(traj[:,-1,:], 2)

################ calculations for metrics ################
### COMPLETION TIME ###
def getCompletionTime():
    diff = np.zeros((agents, timesteps, 3))
    for t in range(0, timesteps):
        diff[:, t, :] = traj[:, t, :] - endPoints
    diff = np.square(diff)
    diff = np.sum(diff, axis=2)
    diff = np.sqrt(diff)

    completionTime = "DNF"
    completionMargin = 0.03
    for t in range(0, timesteps):
        # print(f"{t}:")
        # print(diff[:,t])
        finished = True
        for ag in range(0, agents):
            if diff[ag,t] > completionMargin:
                finished = False
        if finished:
            completionStep = t
            completionTime = completionStep * deltaTime
            return completionStep

### TOTAL DISTANCE ###
def distanceBetweenSteps(arr, t):
    diff = arr[:,t,:] - arr[:,t+1,:]
    diff = np.square(diff)
    diff = np.sum(diff, axis=1)
    diff = np.sqrt(diff)
    diff = np.sum(diff, axis=0)
    return diff

def getEfficiency():
    totalDistance = 0
    completionStep = getCompletionTime()
    for t in range(0, completionStep-1):
        totalDistance += distanceBetweenSteps(traj, t)

    beelineDistance = startPoints - endPoints
    beelineDistance = np.square(beelineDistance)
    beelineDistance = np.sum(beelineDistance, axis=1)
    beelineDistance = np.sqrt(beelineDistance)
    beelineDistance = np.sum(beelineDistance, axis=0)
    
    return beelineDistance / totalDistance
    
### CLOSEST APPROACH ###
def distanceBetweenDrones(arr, t, ag1, ag2):
    dist = arr[ag1,t,:] - arr[ag2,t,:]
    dist = np.square(dist)
    dist = np.sum(dist)
    dist = np.sqrt(dist)
    return dist

def getClosestApproach():
    closestApproach = 99999999
    closestApproachTimestep = -1
    for t in range(0, timesteps):
        for ag1 in range(0, agents):
            for ag2 in range(ag1+1, agents):
                dist = distanceBetweenDrones(traj, t, ag1, ag2)
                if dist < closestApproach:
                    closestApproach = dist
                    closestApproachTimestep = t
    return closestApproach

### LARGEST ACCELERATION ###
def getDiffs(arr):
    diffArr = np.zeros((agents, arr.shape[1]-1, 3))
    for t in range(0, arr.shape[1]-1):
        diffArr[:,t,:] = arr[:,t,:] - arr[:,t+1,:]
    diffArr /= deltaTime
    return diffArr

def getAcc(arr):
    diffArr = np.zeros((agents, timesteps-2, 3))
    for t in range(0, timesteps-2):
        diffArr[:,t,:] = arr[:,t,:] - 2 * arr[:,t+1,:] + arr[:,t+2,:]
    diffArr /= (deltaTime * deltaTime)
    return diffArr

def getAcc1():
    acc = getAcc(traj)
    acc = np.square(acc)
    acc = np.sum(acc, axis=2)
    acc = np.sqrt(acc)

    accMax = 0
    accMaxTimestep = 0
    for t in range(0, timesteps-2):
        for ag in range(0, agents):
            if acc[ag,t] > accMax:
                accMax = acc[ag,t]
                accMaxTimestep = t
    return accMax

def getAcc3():
    acc3 = getDiffs(vel)
    acc3 = np.square(acc3)
    acc3 = np.sum(acc3, axis=2)
    acc3 = np.sqrt(acc3)
    acc3Max = 0
    acc3MaxTimestep = 0
    for t in range(0, timesteps-2):
        for ag in range(0, agents):
            if acc3[ag,t] > acc3Max:
                acc3Max = acc3[ag,t]
                acc3MaxTimestep = t
    return acc3Max

# print("##############")
# print("START POINTS")
# print(startPoints)
# print("END POINTS")
# print(endPoints)

def getResults(delay, run):
    loadTrajectories(delay, run)
    results = [getCompletionTime() * deltaTime, getEfficiency(), getClosestApproach(), getAcc1(), getAcc3()]
    return results

delays = [0, 10, 20, 40, 60, 80, 100]

completeData = np.zeros((len(delays), 5, 10))  # delay, metric, run
for currDelayIndex in range(0, len(delays)):
    currDelay = delays[currDelayIndex]
    results = np.zeros((5, 10))  # 5 = amount of metrics, 10 = amount of runs
    for currRun in range(0, 10):
        results[:,currRun] = getResults(currDelay, currRun+1)
    # print(f"########## RESULTS FOR DELAY {currDelay} ##########")
    # print(results)
    np.save(sys.path[0] + f"/eval/delay_{currDelay}_results.npy", results)
    completeData[currDelayIndex,:,:] = results
print(completeData)
np.save(sys.path[0] + f"/eval/complete_results.npy", completeData)
