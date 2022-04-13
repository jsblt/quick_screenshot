import pyxhook
import time
import datetime as dtm
from datetime import datetime
import pyscreenshot as ImageGrab
from sys import argv
import os

#get directory to save pictures to from one command line argument
_, destination = argv
cwd = os.getcwd()
path = cwd+destination

#make new directory if directory does not exist, otherwise set iterator to current length
#of old directory
isDir = os.path.isdir(cwd+'/'+destination)
if isDir == False:
    path = os.path.join(cwd, destination)
    os.mkdir(path)
    iter = 0
    print("New directory '{}' created in {}".format(destination, cwd))
else:
    print("Extending Directory '{}' in {}".format(destination, cwd))
    iter = len(os.listdir(destination))

#object to save mouse coordinates, time between clicks, picture name iterator,
#save screenshots
class Caller():
    def __init__(self, dest, iter):
        self.clicks = []
        self.coords = []
        self.dif = 2
        self.capture = False
        self.iter = iter
        self.dest = dest

    def clicked(self, event):
        self.coords.append(event.Position)
        if self.dif < 0.4:
            self.capture = True

        if event.MessageName == 'mouse left  down':
            self.clicks.append(datetime.now())
            if len(self.clicks)>1:
                self.dif = (self.clicks[len(self.clicks)-1] - self.clicks[len(self.clicks)-2]).total_seconds()
                if len(self.clicks) > 4:
                    self.clicks = self.clicks[1:]
            else:
                pass

        elif event.MessageName == 'mouse left  up' and self.capture == True:
            a = list(self.coords[-1])
            b = list(self.coords[-2])
            if (a[0] != b[0]) and (a[1] != b[1]):
                area = tuple([min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])])
                print("screenshot")
                img = ImageGrab.grab(bbox=area)
                img.save(self.dest +'/'+str(self.iter)+'.jpg')
                self.iter+=1
            self.capture = False


#instance of caller with target folder and iterator
c = Caller(destination, iter)
parameters={'running':True}
# Create hookmanager
# Define our callback to activate when mouse button goes up or down
hookman = pyxhook.HookManager()
hookman.MouseAllButtonsDown = c.clicked
hookman.MouseAllButtonsUp = c.clicked
hookman.HookMouse()
hookman.start()

# Create a loop to keep the application running
while parameters['running']:
    time.sleep(0.1)
# Close the listener when finished
hookman.cancel()
