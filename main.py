##IMPORT LIBRARIES
from tkinter import messagebox

import plotly.plotly as py## DEN DOYLEYEI XORIS AYTO
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.pyplot as plt
import pylab as p
from matplotlib.widgets import Button
import math
from tkinter.filedialog import askopenfilename, Tk

##CONSTANT VARIEBLES
svp = [611, 657, 706, 758, 813, 872, 935, 1002, 1073, 1148, 1228, 1312, 1402, 1497, 1598, 1705, 1818, 1937, 2064, 2197,
       2338, 2486, 2643, 2809, 2983, 3167, 3361, 3565, 3779, 4005, 4242, 4492, 4754, 5029, 5318, 5621, 5940, 6273, 6623,
       6990, 7374, 7776]

##METHODS DECLARATION
def getSVP(temp):
    y = int(round(temp))
    return svp[y]

def calculateVPD(temp,moist):
    pos = 100 - moist
    svpp = getSVP(temp)
    return (pos / 100) * svpp / 100
def calculateDewpoint(temp,moist):
    pw = (getSVP(temp) * moist / 100) / 100;
    m = 7.591386
    a = 6.116441
    t = 240.7263
    return t / (m / math.log10(pw / a) - 1)
def datetime_to_float(d):
    return d.timestamp()


def getResults(ind):
    plt.clf()
    ##CREATE PLOT
    p.mpl.rcParams['toolbar'] = 'None'

    ##CREATE X AXE AS STRING
    x = [dt.datetime.strptime(d, '%d/%m/%Y %I:%M:%S %p').time() for d in mydates]
    plt.xticks(x, mydates)

    ##GRAB THE LAST TEN RESULTS
    myx = x[(-11+(ind*10)):(-1+(ind*10)):]  ##DATES
    myy = mytemp[(-11+(ind*10)):(-1+(ind*10)):]
    myy2 = mymoist[(-11+(ind*10)):(-1+(ind*10)):]
    mydew = mydewpoint[(-11+(ind*10)):(-1+(ind*10)):]
    myvapor = myvpd[(-11+(ind*10)):(-1+(ind*10)):]

    ##CREATE AXES Y
    ax1 = fig.add_subplot(111)
    ax1.set_ylabel('Temp', color='g')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Moist', color='r')

    ax3 = ax1.twinx()
    ax3.set_ylabel('VPD', color='b')
    ax3.spines['right'].set_position(('outward', 60))

    ##GENATATE PLOT
    ax1.plot(myx, myy, marker='o', color="g", label="temp")
    ax2.plot(myx, myy2, 'r-', marker='o', color="r", label="moist")
    ax3.plot(myx, myvapor, 'r--', marker='o', color="b", label="vpd")

    ##PRINT VALUES ON THE MARKERS
    for i, txt in enumerate(myy):
        ax1.annotate(txt, (myx[i], myy[i]))
    for i, txt in enumerate(myy2):
        ax2.annotate(txt, (myx[i], myy2[i]))
    for i, txt in enumerate(myvapor):
        ax3.annotate(txt, (myx[i], myvapor[i]))

    ##ROTATE X AXE
    for ax in fig.axes:
        p.matplotlib.pyplot.sca(ax)
        plt.xticks(rotation=60)
    plt.tight_layout()

    callback = Index()
    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
    axvpd = plt.axes([0.49, 0.05, 0.1, 0.075])

    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)
    lvpd = Button(axvpd, "Optimal VPD 4-14")

    ##GO FULL SCREEN
    mng = plt.get_current_fig_manager()
    ### does NOT working on ubuntu
    mng.window.state('zoomed')
    plt.show()

##ASK FOR THE FILE
Tk().withdraw()
filename = askopenfilename()

#GENERATE DATA FROM FILE AND SAVE TO ARRAYS
f = open(filename, encoding="utf-16")
mytemp = []
mydates = []
mymoist = []
myvpd=[]
mydewpoint=[]
for line in f:
    inputrow = line.split(";")
    ##ADD RAW DATA
    mytemp.append(float(inputrow[2]))
    mydates.append(inputrow[1])
    mymoist.append(float(inputrow[3]))
    ##ADD CALCULATED DATA
    myvpd.append(int(round(calculateVPD(float(inputrow[2]),float(inputrow[3])))))
    mydewpoint.append(calculateDewpoint(float(inputrow[2]),float(inputrow[3])))


##DISABLE OFICIAL TOOLBAR
p.mpl.rcParams['toolbar'] = 'None'

##CREATE PLOT
fig = plt.figure()

##CREATE X AXE AS STRING
x = [dt.datetime.strptime(d, '%d/%m/%Y %I:%M:%S %p').time() for d in mydates]
plt.xticks(x, mydates)

##GRAB THE LAST TEN RESULTS
myx = x[-11:-1:]##DATES
myy = mytemp[-11:-1:]
myy2 = mymoist[-11:-1:]
mydew=mydewpoint[-11:-1:]
myvapor=myvpd[-11:-1:]

##CREATE AXES Y
ax1 = fig.add_subplot(111)
ax1.set_ylabel('Temp' ,color='g')

ax2 = ax1.twinx()
ax2.set_ylabel('Moist', color='r')

ax3=ax1.twinx()
ax3.set_ylabel('VPD', color='b')
ax3.spines['right'].set_position(('outward', 60))

##GENATATE PLOT
ax1.plot(myx, myy, marker='o',color="g",label="temp")
ax2.plot(myx, myy2, 'r-', marker='o',color="r",label="moist")
ax3.plot(myx, myvapor, 'r--', marker='o',color="b",label="vpd")

##PRINT VALUES ON THE MARKERS
for i, txt in enumerate(myy):
    ax1.annotate(txt, (myx[i],myy[i]))
for i, txt in enumerate(myy2):
    ax2.annotate(txt, (myx[i],myy2[i]))
for i, txt in enumerate(myvapor):
    ax3.annotate(txt, (myx[i],myvapor[i]))

##ROTATE X AXE
for ax in fig.axes:
    p.matplotlib.pyplot.sca(ax)
    plt.xticks(rotation=60)
plt.tight_layout()


#BUTTON DECLARATION , POSITTION AND EVENT HANDLING
class Index(object):
    ind =0

    def next(self, event):
        if(self.ind==0):
            messagebox.showinfo("Title", "a Tk MessageBox")

    def prev(self, event):
        getResults(self.ind)
        self.ind += 1
        print(self.ind)
        print("sad")




callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
axvpd = plt.axes([0.49, 0.05, 0.1, 0.075])

bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)
lvpd=Button(axvpd,"Optimal VPD 4-14")



##GO FULL SCREEN
mng = plt.get_current_fig_manager()
### does NOT working on ubuntu
mng.window.state('zoomed')


##DISPLAY PLOT

plt.show()

