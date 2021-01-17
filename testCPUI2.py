from PyQt5.QtWidgets import QApplication

import tello
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import traceback, sys

# Create Billy
global billy
billy = tello.Tello()
# Put Tello into command mode
billy.send("command", 3)

previ = 0

# directional counts
upcount = 0
downcount = 0
forwardcount = 0
backwardcount = 0
leftcount = 0
rightcount = 0

# Flip counts
flpl = 0
flpr = 0
flpf = 0
flpb = 0

# Rotation counts
clkw = 0
cclkw = 0

override_chck = 0
takeoff_chck = 0

persweepclicked = 0

manucontrol = 1

referarr = []
print("Drone is in Manual Mode.")


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)


class Ui_MainWindow(object):

    def __init__(self, *args, **kwargs):
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    # --------------------------------------------Manual Control Methods----------------------------------------------------
    # takeoff
    def takeoff(self):
        billy.send("takeoff", 7)
        global takeoff_chck
        takeoff_chck = 1

    # land
    def land(self):
        if manucontrol == 1 or override_chck == 1:
            billy.send("land", 3)
        else:
            print("You are in Autonomous mode.")

        # Close the socket
        # billy.sock.close() [Causes error as it is not connected with real drone]

    # Stop in Air
    def stopinair(self):
        if manucontrol == 1 or override_chck == 1:
            billy.send("stop", 3)
        else:
            print("You are in Autonomous mode.")

    # ----------------------------------------------Directional Methods----------------------------------------------
    def forward(self):
        if override_chck == 1:
            global forwardcount
            forwardcount += 1
            referarr.append("f")
            billy.send("forward 80", 5)
            return
        elif manucontrol == 1:
            billy.send("forward 80", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    def back(self):
        if override_chck == 1:
            global backwardcount
            backwardcount += 1
            referarr.append("b")
            billy.send("back 80", 5)
            return
        elif manucontrol == 1:
            billy.send("back 80", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    def left(self):
        if override_chck == 1:
            global leftcount
            leftcount += 1
            referarr.append("l")
            billy.send("left 80", 5)
            return
        elif manucontrol == 1:
            billy.send("left 80", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    def right(self):
        if override_chck == 1:
            global rightcount
            referarr.append("r")
            rightcount += 1
            billy.send("right 80", 5)
            return
        elif manucontrol == 1:
            billy.send("right 80", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    def up(self):
        if override_chck == 1:
            global upcount
            upcount += 1
            referarr.append("u")
            billy.send("up 50", 5)
            return
        elif manucontrol == 1:
            billy.send("up 50", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    def down(self):
        if override_chck == 1:
            global downcount
            downcount += 1
            referarr.append("d")
            billy.send("down 50", 5)
            return
        elif manucontrol == 1:
            billy.send("down 50", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    # ------------------------------------------Flip Methods-------------------------------------------------
    def flipleft(self):
        if override_chck == 1:
            global flpl
            flpl += 1
            referarr.append("flpl")
            billy.send("flip l", 5)
            return
        elif manucontrol == 1:
            billy.send("flip l", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    def flipright(self):
        if override_chck == 1:
            global flpr
            flpr += 1
            referarr.append("flpr")
            billy.send("flip r", 5)
            return
        elif manucontrol == 1:
            billy.send("flip r", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    def flipforward(self):
        if override_chck == 1:
            global flpf
            flpf += 1
            referarr.append("flpf")
            billy.send("flip f", 5)
            return
        elif manucontrol == 1:
            billy.send("flip f", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    def flipback(self):
        if override_chck == 1:
            global flpb
            flpb += 1
            referarr.append("flpb")
            billy.send("flip b", 5)
            return
        elif manucontrol == 1:
            billy.send("flip b", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    # ------------------------------------Rotational Methods--------------------------------------
    def cw(self):
        if override_chck == 1:
            global clkw
            clkw += 1
            referarr.append("clkw")
            billy.send("cw 30", 5)
            return
        elif manucontrol == 1:
            billy.send("cw 30", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    def ccw(self):
        if override_chck == 1:
            global cclkw
            cclkw += 1
            referarr.append("cclkw")
            billy.send("ccw 30", 5)
            return
        elif manucontrol == 1:
            billy.send("ccw 30", 5)
            return
        elif manucontrol == 0:
            print("You are in Autonomous mode.")
            return

    # ------------------------------------Speed Methods--------------------------------------------
    def highspeed(self):
        if manucontrol == 1 or override_chck == 1:
            billy.send("speed 100", 5)
        else:
            print("You are in Autonomous mode.")

    def lowspeed(self):
        if manucontrol == 1 or override_chck == 1:
            billy.send("speed 30", 5)
        else:
            print("You are in Autonomous mode.")

    # ----------------------------- Overriding perimeter sweep and also going back to the place where drone stopped------------------------------
    def override(self):
        global referarr
        global override_chck
        global previ
        if override_chck == 0:
            override_chck = 1
            return
        elif override_chck == 1:
            override_chck = 0
            print()
            print("i was "+str(previ))
            print("Going back to the point where perimeter sweep was overriden.")
            referarr.reverse()
            for r in range(0,len(referarr)):
                if referarr[r] == "u":
                    self.down()
                elif referarr[r] == "d":
                    self.up()
                elif referarr[r] == "l":
                    self.right()
                elif referarr[r] == "r":
                    self.left()
                elif referarr[r] == "f":
                    self.back()
                elif referarr[r] == "b":
                    self.forward()
                elif referarr[r] == "clkw":
                    self.ccw()
                elif referarr[r] == "cclkw":
                    self.cw()
                elif referarr[r] == "flipf":
                    self.flipback()
                elif referarr[r] == "flipb":
                    self.flipforward()
                elif referarr[r] == "flipl":
                    self.flipright()
                elif referarr[r] == "flipr":
                    self.flipleft()
            print("Reached the point where perimeter sweep was overriden.")
            referarr=[]
            print()
            print("Continuing perimeter sweep.")
            self.persweepcont_exec()

    # ------------------------------------------------Perimeter sweep-------------------------------------------------------
    def persweep(self):
        global previ
        print("Manual Mode switched off.")
        print("Manual Controls locked.")
        print("Autonomous Mode started.")
        global manucontrol
        manucontrol -= 1
        # Travel to/from starting checkpoint 0 from/to the charging base
        frombase = ["forward", 50, "ccw", 150]
        tobase = ["ccw", 150, "forward", 50]

        # Flight path to Checkpoint 1 to 5 and back to Checkpoint 0 sequentially
        checkpoint = [[1, "cw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
                      [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]

        print("Perimeter sweep started.")

        # Send the takeoff command
        if takeoff_chck == 0:
            billy.send("takeoff", 7)

        print("\n")

        # Start at checkpoint 1 and print destination
        print("From the charging base to the starting checkpoint of sweep pattern.\n")

        billy.send(frombase[0] + " " + str(frombase[1]), 4)
        billy.send(frombase[2] + " " + str(frombase[3]), 4)

        print("Current location: Checkpoint 0 " + "\n")

        # Billy's flight path
        for i in range(len(checkpoint)):
            QApplication.processEvents()
            if i == len(checkpoint) - 1:
                print("Returning to Checkpoint 0. \n")
                previ=0
            if override_chck == 1:
                print("Manual mode initiated.")
                manucontrol = 1
                return

            billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
            billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

            print("Arrived at current location: Checkpoint " + str(checkpoint[i][0]) + "\n")

            previ = i
            time.sleep(4)

        # Reach back at Checkpoint 0
        print("Complete sweep. Return to charging base.\n")
        billy.send(tobase[0] + " " + str(tobase[1]), 4)
        billy.send(tobase[2] + " " + str(tobase[3]), 4)

        # Turn to original direction before land
        print("Turn to original direction before land.\n")
        billy.send("cw 180", 4)

        # Land
        billy.send("land", 3)

        # Close the socket
        # billy.sock.close() [Causes error as it is not connected with real drone]
        print("Perimeter sweep completed successfully.")
        print("Autonomous mode switched off.")
        print("You are now in manual mode.")
        manucontrol += 1

    def persweep_exec(self):
        # Pass the function to execute
        worker = Worker(self.persweep)  # Any other args, kwargs are passed to the run function

        # Execute
        self.threadpool.start(worker)

    def persweepcontinue(self):
        global previ
        # Travel to/from starting checkpoint 0 from/to the charging base
        frombase = ["forward", 50, "ccw", 150]
        tobase = ["ccw", 150, "forward", 50]

        # Flight path to Checkpoint 1 to 5 and back to Checkpoint 0 sequentially
        checkpoint = [[1, "cw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
                      [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]
        i = previ
        print("Current location: Checkpoint " + str(checkpoint[i][0]) + "\n")
        i+=1
        # Billy's flight path
        while i < len(checkpoint):
            print("test i"+str(i))
            if i == len(checkpoint) - 1:
                print("Returning to Checkpoint 0. \n")

            billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
            billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

            print("Arrived at current location: Checkpoint " + str(checkpoint[i][0]) + "\n")
            i+=1
            time.sleep(4)

        # Reach back at Checkpoint 0
        print("Complete sweep. Return to charging base.\n")
        billy.send(tobase[0] + " " + str(tobase[1]), 4)
        billy.send(tobase[2] + " " + str(tobase[3]), 4)

        # Turn to original direction before land
        print("Turn to original direction before land.\n")
        billy.send("cw 180", 4)

        # Land
        billy.send("land", 3)

        # Close the socket
        # billy.sock.close() [Causes error as it is not connected with real drone]
        print("Perimeter sweep completed successfully.")

    def persweepcont_exec(self):
        # Pass the function to execute
        worker = Worker(self.persweepcontinue)  # Any other args, kwargs are passed to the run function

        # Execute
        self.threadpool.start(worker)
    # -------------------------------------------emergency------------------------------
    def emergency(self):
        # Send the emergency stop command
        billy.send("emergency", 3)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color:rgb(248, 249, 255)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fbtn = QtWidgets.QPushButton(self.centralwidget)
        self.fbtn.setGeometry(QtCore.QRect(490, 40, 81, 111))
        self.fbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fbtn.setStyleSheet("background-color: rgb(139, 139, 139);\n"
                                "color: white;")
        self.fbtn.setObjectName("fbtn")
        self.bcbtn = QtWidgets.QPushButton(self.centralwidget)
        self.bcbtn.setGeometry(QtCore.QRect(490, 230, 81, 111))
        self.bcbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bcbtn.setStyleSheet("background-color: rgb(139, 139, 139);\n"
                                 "color: white;")
        self.bcbtn.setObjectName("bcbtn")
        self.rbtn = QtWidgets.QPushButton(self.centralwidget)
        self.rbtn.setGeometry(QtCore.QRect(570, 150, 111, 81))
        self.rbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.rbtn.setStyleSheet("background-color: rgb(139, 139, 139);\n"
                                "color: white;")
        self.rbtn.setObjectName("rbtn")
        self.lbtn = QtWidgets.QPushButton(self.centralwidget)
        self.lbtn.setGeometry(QtCore.QRect(380, 150, 111, 81))
        self.lbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lbtn.setStyleSheet("background-color: rgb(139, 139, 139);\n"
                                "color: white;")
        self.lbtn.setObjectName("lbtn")
        self.peribtn = QtWidgets.QPushButton(self.centralwidget)
        self.peribtn.setGeometry(QtCore.QRect(10, 450, 211, 91))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.peribtn.setFont(font)
        self.peribtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.peribtn.setStyleSheet("background-color: rgb(0, 170, 255);\n"
                                   "color: white;\n"
                                   "border-radius: 20px;")
        self.peribtn.setObjectName("peribtn")
        self.overrbtn = QtWidgets.QPushButton(self.centralwidget)
        self.overrbtn.setGeometry(QtCore.QRect(590, 450, 201, 91))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.overrbtn.setFont(font)
        self.overrbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.overrbtn.setStyleSheet("background-color: rgb(255, 206, 56);\n"
                                    "color: white;\n"
                                    "border-radius: 20px;")
        self.overrbtn.setObjectName("overrbtn")
        self.labelmanu = QtWidgets.QLabel(self.centralwidget)
        self.labelmanu.setGeometry(QtCore.QRect(330, -10, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelmanu.setFont(font)
        self.labelmanu.setObjectName("labelmanu")
        self.envidbtn = QtWidgets.QPushButton(self.centralwidget)
        self.envidbtn.setGeometry(QtCore.QRect(320, 410, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.envidbtn.setFont(font)
        self.envidbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.envidbtn.setStyleSheet("background-color: rgb(68, 68, 68);\n"
                                    "color: white;\n"
                                    "border-radius: 20px;")
        self.envidbtn.setObjectName("envidbtn")
        self.takeoffbtn = QtWidgets.QPushButton(self.centralwidget)
        self.takeoffbtn.setGeometry(QtCore.QRect(10, 60, 121, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.takeoffbtn.setFont(font)
        self.takeoffbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.takeoffbtn.setStyleSheet("background-color: rgb(0, 202, 0);\n"
                                      "color: white;\n"
                                      "border-radius: 70px;")
        self.takeoffbtn.setObjectName("takeoffbtn")
        self.emergstopbtn = QtWidgets.QPushButton(self.centralwidget)
        self.emergstopbtn.setGeometry(QtCore.QRect(10, 370, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.emergstopbtn.setFont(font)
        self.emergstopbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.emergstopbtn.setStyleSheet("background-color: rgb(255, 32, 32);\n"
                                        "color: white;\n"
                                        "border-radius: 70px;")
        self.emergstopbtn.setObjectName("emergstopbtn")
        self.upbtn = QtWidgets.QPushButton(self.centralwidget)
        self.upbtn.setGeometry(QtCore.QRect(730, 40, 51, 111))
        self.upbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.upbtn.setStyleSheet("background-color: rgb(139, 139, 139);\n"
                                 "color: white;")
        self.upbtn.setObjectName("upbtn")
        self.downbtn = QtWidgets.QPushButton(self.centralwidget)
        self.downbtn.setGeometry(QtCore.QRect(730, 160, 51, 111))
        self.downbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.downbtn.setStyleSheet("background-color: rgb(139, 139, 139);\n"
                                   "color: white;")
        self.downbtn.setObjectName("downbtn")
        self.cwbtn = QtWidgets.QPushButton(self.centralwidget)
        self.cwbtn.setGeometry(QtCore.QRect(610, 310, 81, 31))
        self.cwbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cwbtn.setStyleSheet("background-color: rgb(139, 139, 139);\n"
                                 "color: white;")
        self.cwbtn.setObjectName("cwbtn")
        self.ccwbtn = QtWidgets.QPushButton(self.centralwidget)
        self.ccwbtn.setGeometry(QtCore.QRect(700, 310, 81, 31))
        self.ccwbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ccwbtn.setStyleSheet("background-color: rgb(139, 139, 139);\n"
                                  "color: white;")
        self.ccwbtn.setObjectName("ccwbtn")
        self.pauseBtn = QtWidgets.QPushButton(self.centralwidget)
        self.pauseBtn.setGeometry(QtCore.QRect(10, 160, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pauseBtn.setFont(font)
        self.pauseBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pauseBtn.setStyleSheet("background-color: rgb(255, 206, 56);\n"
                                    "color: white;\n"
                                    "border-radius: 20px;")
        self.pauseBtn.setObjectName("pauseBtn")
        self.disvidbtn = QtWidgets.QPushButton(self.centralwidget)
        self.disvidbtn.setGeometry(QtCore.QRect(320, 480, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.disvidbtn.setFont(font)
        self.disvidbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.disvidbtn.setStyleSheet("background-color: rgb(68, 68, 68);\n"
                                     "color: white;\n"
                                     "border-radius: 20px;")
        self.disvidbtn.setObjectName("disvidbtn")
        self.landbtn = QtWidgets.QPushButton(self.centralwidget)
        self.landbtn.setGeometry(QtCore.QRect(10, 260, 121, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.landbtn.setFont(font)
        self.landbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.landbtn.setStyleSheet("background-color: rgb(0, 202, 0);\n"
                                   "color: white;\n"
                                   "border-radius: 70px;")
        self.landbtn.setObjectName("landbtn")
        self.fliplbtn = QtWidgets.QPushButton(self.centralwidget)
        self.fliplbtn.setGeometry(QtCore.QRect(210, 60, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.fliplbtn.setFont(font)
        self.fliplbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fliplbtn.setStyleSheet("background-color: rgb(68, 68, 68);\n"
                                    "color: white;\n"
                                    "border-radius: 20px;")
        self.fliplbtn.setObjectName("fliplbtn")
        self.fliprbtn = QtWidgets.QPushButton(self.centralwidget)
        self.fliprbtn.setGeometry(QtCore.QRect(310, 60, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.fliprbtn.setFont(font)
        self.fliprbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fliprbtn.setStyleSheet("background-color: rgb(68, 68, 68);\n"
                                    "color: white;\n"
                                    "border-radius: 20px;")
        self.fliprbtn.setObjectName("fliprbtn")
        self.flipfwbtn = QtWidgets.QPushButton(self.centralwidget)
        self.flipfwbtn.setGeometry(QtCore.QRect(210, 130, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.flipfwbtn.setFont(font)
        self.flipfwbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.flipfwbtn.setStyleSheet("background-color: rgb(68, 68, 68);\n"
                                     "color: white;\n"
                                     "border-radius: 20px;")
        self.flipfwbtn.setObjectName("flipfwbtn")
        self.flipbwbtn = QtWidgets.QPushButton(self.centralwidget)
        self.flipbwbtn.setGeometry(QtCore.QRect(210, 180, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.flipbwbtn.setFont(font)
        self.flipbwbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.flipbwbtn.setStyleSheet("background-color: rgb(68, 68, 68);\n"
                                     "color: white;\n"
                                     "border-radius: 20px;")
        self.flipbwbtn.setObjectName("flipbwbtn")
        self.hspeedbtn = QtWidgets.QPushButton(self.centralwidget)
        self.hspeedbtn.setGeometry(QtCore.QRect(200, 280, 111, 61))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.hspeedbtn.setFont(font)
        self.hspeedbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hspeedbtn.setStyleSheet("background-color: rgb(0, 170, 255);\n"
                                     "color: white;\n"
                                     "border-radius: 20px;")
        self.hspeedbtn.setObjectName("hspeedbtn")
        self.lspeedbtn = QtWidgets.QPushButton(self.centralwidget)
        self.lspeedbtn.setGeometry(QtCore.QRect(330, 280, 111, 61))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lspeedbtn.setFont(font)
        self.lspeedbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lspeedbtn.setStyleSheet("background-color: rgb(0, 170, 255);\n"
                                     "color: white;\n"
                                     "border-radius: 20px;")
        self.lspeedbtn.setObjectName("lspeedbtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # -------------------------------Connecting takeoff method to takeoff button---------------------------------
        self.takeoffbtn.clicked.connect(self.takeoff)
        # --------------------------------Connecting land method to land button-----------------------------------
        self.landbtn.clicked.connect(self.land)
        # -------------------------------Connecting persweep method to persweep button---------------------------------
        self.peribtn.clicked.connect(self.persweep_exec)
        # -------------------------------Connecting emergency method to emergstop button-------------------------------
        self.emergstopbtn.clicked.connect(self.emergency)
        # -------------------------------Connecting pause method to pause button---------------------------------
        self.pauseBtn.clicked.connect(self.stopinair)
        # -------------------------------Connecting directional method to directional buttons--------------------------
        self.upbtn.clicked.connect(self.up)
        self.downbtn.clicked.connect(self.down)
        self.fbtn.clicked.connect(self.forward)
        self.bcbtn.clicked.connect(self.back)
        self.lbtn.clicked.connect(self.left)
        self.rbtn.clicked.connect(self.right)
        # -------------------------------Connecting flip methods to flip buttons--------------------------
        self.flipfwbtn.clicked.connect(self.flipforward)
        self.flipbwbtn.clicked.connect(self.flipback)
        self.fliprbtn.clicked.connect(self.flipright)
        self.fliplbtn.clicked.connect(self.flipleft)
        # -------------------------------Connecting Rotation methods to rotation buttons--------------------------
        self.cwbtn.clicked.connect(self.cw)
        self.ccwbtn.clicked.connect(self.ccw)
        # -------------------------------Connecting Speed methods to speed buttons--------------------------
        self.hspeedbtn.clicked.connect(self.highspeed)
        self.lspeedbtn.clicked.connect(self.lowspeed)

        # -------------------------------Connecting override method to override button--------------------------
        self.overrbtn.clicked.connect(self.override)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tello Drone Control Panel"))
        self.fbtn.setText(_translate("MainWindow", "FORWARD"))
        self.bcbtn.setText(_translate("MainWindow", "BACKWARD"))
        self.rbtn.setText(_translate("MainWindow", "RIGHT"))
        self.lbtn.setText(_translate("MainWindow", "LEFT"))
        self.peribtn.setText(_translate("MainWindow", "PERIMETER SWEEP"))
        self.overrbtn.setText(_translate("MainWindow", "OVERRIDE ROUT"))
        self.labelmanu.setText(_translate("MainWindow", "Control Panel"))
        self.envidbtn.setText(_translate("MainWindow", "Enable Video Stream"))
        self.takeoffbtn.setText(_translate("MainWindow", "TAKEOFF"))
        self.emergstopbtn.setText(_translate("MainWindow", "Emergency stop"))
        self.upbtn.setText(_translate("MainWindow", "UP"))
        self.downbtn.setText(_translate("MainWindow", "Down"))
        self.cwbtn.setText(_translate("MainWindow", "CW"))
        self.ccwbtn.setText(_translate("MainWindow", "CCW"))
        self.pauseBtn.setText(_translate("MainWindow", "Pause"))
        self.disvidbtn.setText(_translate("MainWindow", "Disable Video Stream"))
        self.landbtn.setText(_translate("MainWindow", "Land"))
        self.fliplbtn.setText(_translate("MainWindow", "Flip Left"))
        self.fliprbtn.setText(_translate("MainWindow", "Flip Right"))
        self.flipfwbtn.setText(_translate("MainWindow", "Flip FW"))
        self.flipbwbtn.setText(_translate("MainWindow", "Flip BW"))
        self.hspeedbtn.setText(_translate("MainWindow", "High Speed"))
        self.lspeedbtn.setText(_translate("MainWindow", "Low Speed"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
