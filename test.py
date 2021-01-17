from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys
import tello
# Create Billy
global billy
billy = tello.Tello()
# Put Tello into command mode
billy.send("command", 3)

prevI = 0
checkpointholder = 0
upcount = 0
downcount = 0
forwardcount = 0
backwardcount = 0
leftcount = 0
rightcount = 0
override_chck = 0
takeoff_chck = 0

persweepclicked = 0

manucontrol = 1

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


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
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done



class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0

        layout = QVBoxLayout()

        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        worker = Worker(self.persweep)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)


    def persweep(self,progress_callback):

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
        if takeoff_chck==0:
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

            billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
            billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

            print("Arrived at current location: Checkpoint " + str(checkpoint[i][0]) + "\n")
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
    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            #progress_callback.emit(n*100/4)

        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)


    def recurring_timer(self):
        self.counter +=1
        self.l.setText("Counter: %d" % self.counter)


app = QApplication([])
window = MainWindow()
app.exec_()