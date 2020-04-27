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
        self.delay = 0


    def recordDronesTask(self, task):
        self.now = datetime.datetime.now()
        delta = self.now - self.prev
        if self.delay < 10:
            self.delay += 1
        else:
            self.tAccum += delta.total_seconds()
            self.amount += 1
            print(self.tAccum / self.amount)
        self.prev = datetime.datetime.now()

        task.delayTime = 0.05
        self.recordingLstPos.append(self.droneManager.getAllPositions())
        if self.recordVelocity:
            self.recordingLstVel.append(self.droneManager.getAllVelocities())
        return task.again


    def save(self):
        delay = 0
        run = 1

        posTraj = np.asarray(self.recordingLstPos)
        posTraj = np.swapaxes(posTraj, 0, 1)  # make array in the shape agent, timestep, dimension
        np.save(sys.path[0] + f"/trajectories/4quads/{delay}/pos_traj_{run}.npy", posTraj)
        if self.recordVelocity:
            velTraj = np.asarray(self.recordingLstVel)
            velTraj = np.swapaxes(velTraj, 0, 1)  # make array in the shape agent, timestep, dimension
            np.save(sys.path[0] + f"/trajectories/4quads/{delay}/vel_traj_{run}.npy", velTraj)
        print("recording saved")


    def toggleRecording(self):
        if not self.isRecording:
            print("recording started")
            self.recordingLstPos = []
            self.recordingLstVel = []
            self.isRecording = True
            self.droneManager.base.taskMgr.doMethodLater(0, self.recordDronesTask, "RecordDrones")
        else:
            self.tAccum = 0
            self.amount = 0
            self.delay = 0
            
            self.isRecording = False
            self.droneManager.base.taskMgr.remove("RecordDrones")
            self.save()
            # self.recordingLst = []
            # self.recordingLstVel = []
