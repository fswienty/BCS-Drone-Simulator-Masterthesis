import os
import sys
import numpy as np
import datetime
from direct.showbase import DirectObject


class DroneRecorder(DirectObject.DirectObject):

    def __init__(self, droneManager):
        self.droneManager = droneManager
        self.recordingLstPos = []
        self.recordingLstVel = []
        self.isRecording = False
        self.accept('space', self.toggleRecording)
        self.recordVelocity = True

        self.now = datetime.datetime.now()
        self.prev = datetime.datetime.now()
        self.tAccum = 0
        self.amount = 0


    def recordDronesTask(self, task):

        self.now = datetime.datetime.now()
        delta = self.now - self.prev
        if self.amount > 10:
            self.tAccum += delta.total_seconds()
        self.amount += 1
        if self.amount > 10:
            print(self.tAccum / (self.amount - 10))
        self.prev = datetime.datetime.now()


        task.delayTime = 0.05
        self.recordingLstPos.append(self.droneManager.getAllPositions())
        if self.recordVelocity:
            self.recordingLstVel.append(self.droneManager.getAllVelocities())
        return task.again


    def save(self):
        posTraj = np.asarray(self.recordingLstPos)
        posTraj = np.swapaxes(posTraj, 0, 1)  # make array in the shape agent, timestep, dimension
        np.save(sys.path[0] + "/trajectories/pos_traj.npy", posTraj)
        if self.recordVelocity:
            velTraj = np.asarray(self.recordingLstVel)
            velTraj = np.swapaxes(velTraj, 0, 1)  # make array in the shape agent, timestep, dimension
            np.save(sys.path[0] + "/trajectories/vel_traj.npy", velTraj)
        print("recording saved")


    def toggleRecording(self):
        if not self.isRecording:
            print("recording started")
            self.isRecording = True
            self.droneManager.base.taskMgr.doMethodLater(0, self.recordDronesTask, "RecordDrones")
        else:
            self.isRecording = False
            self.droneManager.base.taskMgr.remove("RecordDrones")
            self.save()
            # self.recordingLst = []
            # self.recordingLstVel = []
