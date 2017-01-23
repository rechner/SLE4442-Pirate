#!/usr/bin/env python

import imp
import sys
import Tkinter
import ttk
import tkMessageBox

#from Module.LogViewer.LogView import *
#from TKGui.HexViewer import *
from config import configManager  # Import and init the configuration manager singleton
from hexview import HexViewer, HexViewControl
from asciiview import ASCIIViewControl
from dataset import Dataset
from dispatcher import dispatcher, DEvent
from h0xview import H0xView

import readcard


class App():
    def __init__(self):
        configManager.load_config()
        self.modules = []  # A list of all currently loaded modules
        self.dataset = None  # This is the currently loaded dataset

        self.view = H0xView()

        dispatcher.add_event_listener("CONTROL_EXIT", self.quit)
        dispatcher.add_event_listener("CONTROL_SAVEAS", self.saveas)
        #dispatcher.add_event_listener("CONTROL_SAVE", self.open)
        dispatcher.add_event_listener("CONTROL_OPEN", self.open)
        dispatcher.add_event_listener("CONTROL_UNDO", self.undo)
        dispatcher.add_event_listener("CONTROL_REDO", self.redo)
        dispatcher.add_event_listener("CONTROL_CUT", self.open)
        dispatcher.add_event_listener("CONTROL_COPY", self.open)
        dispatcher.add_event_listener("CONTROL_PASTE", self.open)
        dispatcher.add_event_listener("CONTROL_INSERT", self.open)
        dispatcher.add_event_listener("CONTROL_HELP", self.open)
        dispatcher.add_event_listener("CONTROL_ABOUT", self.open)
        dispatcher.add_event_listener("READ_CARD", self.read_card)
        dispatcher.add_event_listener("READ_ATR", self.read_ATR)
        #self.root.resizable(True, False)

        #self.tabControl = ttk.Notebook(self.root)
        #self.tabControl.grid(sticky=N+S+E+W)


        ##module_list = configManager.get_config("MODULES", [])
        ##self.initialise_modules(module_list)

        #self.initialiseLogView()
        #self.initialiseProxy()
        #self.initialiseHistory()

        #self.testframe = ScapyDataFrame(master=self.root)
        #self.tabControl.add(self.testframe, text="Test")


        # Initialise hexviewer
        hvc = HexViewControl(self)
        hvc.initialise()
        avc = ASCIIViewControl(self)
        avc.initialise()


        self.update_clock()

        self.pirate = readcard.get_device()

        try:
            self.view.root.mainloop()
        except KeyboardInterrupt:
            #self.pserver.close()
            self.quit()

    def update_clock(self):
        """  Kind of like our main loop, call our-self again after a time in ms """
        self.view.root.after(200, self.update_clock)
        #for module in self.modules:
        #    module.update()

    def quit(self, *args):
        self.pirate.iostream.close()
        sys.exit()

    def read_ATR(self, event):
        atr = readcard.get_atr(self.pirate)
        tkMessageBox.showinfo("ATR", " ".join(atr))

    def read_card(self, event):
        hex_data = readcard.read_card(self.pirate)
        byte_data = readcard.hex_to_bytes(hex_data)

        print(hex_data)

        if len(hex_data) == 0:
            tkMessageBox.showerror("Card Read Error", "Error while reading card: parse error or no data returned")
            return

        self.dataset = Dataset(byte_data)

        evt = DEvent("LOAD_DATASET", {"dataset": self.dataset})
        dispatcher.dispatch_event(evt)


    def open(self, event):
        filename = event.data['filename']
        with open(filename, mode='rb', buffering=0) as file:
            self.dataset = Dataset(initial_data=file.read())

        evt = DEvent("LOAD_DATASET", {"dataset": self.dataset})
        dispatcher.dispatch_event(evt)

    def saveas(self, event):
        if self.dataset is None:
            raise Exception("Cannot save, dataset is None")

        filename = event.data['filename']
        try:
            file = open(filename, 'wb')
            file.write(self.dataset.data)
            file.close()
        except Exception as e:
            print("FAILED TO SAVE: %s" % (e))
            raise

    def undo(self, event):
        if self.dataset is None:
            raise Exception("Cannot undo, dataset is None")

        self.dataset.undo()
        evt = DEvent("UPDATE_DATASET", {})
        dispatcher.dispatch_event(evt)

    def redo(self, event):
        if self.dataset is None:
            raise Exception("Cannot redo, dataset is None")

        self.dataset.redo()
        evt = DEvent("UPDATE_DATASET", {})
        dispatcher.dispatch_event(evt)

    #def initialise_modules(self, moduleList):
    #    for module in moduleList:
    #        moduleName = module['MODULENAME']
    #        print("Loading module '%s'"%moduleName)
    #        fp, pathname, description = imp.find_module(moduleName, ["Module"])
    #        module = imp.load_module(moduleName, fp, pathname, description)
    #        module.initialise(self)
    #
    #        self.modules.append(module)

    #def updateProxy(self):
    #    self.proxyControl.update()



if __name__ == "__main__":
    app = App()


