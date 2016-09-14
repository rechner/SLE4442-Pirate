
import imp
import sys
import Tkinter
import ttk
import tkFileDialog

#from Module.LogViewer.LogView import *
#from TKGui.HexViewer import *
from config import configManager  # Import and init the configuration manager singleton
from hexview import HexViewer, HexViewControl
from dataset import Dataset
from dispatcher import dispatcher, DEvent


class H0xView(object):
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.title("h0x")
        self.initialise_window()

    def on_new(self):
        evt = DEvent("CONTROL_NEW", {})
        dispatcher.dispatch_event(evt)

    def on_open(self):
        file_opt = options = {}
        options['defaultextension'] = ''
        options['filetypes'] = [('all files', '.*')]
        options['initialdir'] = configManager.get_config("INITIAL_DIR", '\\')
        options['initialfile'] = configManager.get_config("INITIAL_FILE", 'myfile.hex')
        options['parent'] = self.root
        options['title'] = 'Open'
        filename = tkFileDialog.askopenfilename(**file_opt)

        # If no file selected
        if filename == "":
            return

        evt = DEvent("CONTROL_OPEN", {"filename":filename})
        dispatcher.dispatch_event(evt)

    def on_save(self):
        pass

    def on_saveas(self):
        file_opt = options = {}
        options['defaultextension'] = ''
        options['filetypes'] = [('all files', '.*')]
        options['initialdir'] = configManager.get_config("INITIAL_DIR", '\\')
        options['initialfile'] = configManager.get_config("INITIAL_FILE", 'myfile.hex')
        options['parent'] = self.root
        options['title'] = 'Save'
        filename = tkFileDialog.asksaveasfilename(**file_opt)

        # If no file selected
        if filename == "":
            return

        evt = DEvent("CONTROL_SAVEAS", {"filename":filename})
        dispatcher.dispatch_event(evt)

    def on_exit(self):
        evt = DEvent("CONTROL_EXIT", {})
        dispatcher.dispatch_event(evt)

    def on_undo(self):
        evt = DEvent("CONTROL_UNDO", {})
        dispatcher.dispatch_event(evt)

    def on_redo(self):
        evt = DEvent("CONTROL_REDO", {})
        dispatcher.dispatch_event(evt)

    def on_cut(self):
        evt = DEvent("CONTROL_CUT", {})
        dispatcher.dispatch_event(evt)

    def on_copy(self):
        evt = DEvent("CONTROL_COPY", {})
        dispatcher.dispatch_event(evt)

    def on_paste(self):
        evt = DEvent("CONTROL_PASTE", {})
        dispatcher.dispatch_event(evt)

    def on_delete(self):
        evt = DEvent("CONTROL_INSERT", {})
        dispatcher.dispatch_event(evt)

    def on_find(self):
        evt = DEvent("CONTROL_FIND", {})
        dispatcher.dispatch_event(evt)

    def on_findnext(self):
        evt = DEvent("CONTROL_FINDNEXT", {})
        dispatcher.dispatch_event(evt)

    def on_selectall(self):
        evt = DEvent("CONTROL_SELECTALL", {})
        dispatcher.dispatch_event(evt)

    def on_preferences(self):
        evt = DEvent("CONTROL_PREFERENCES", {})
        dispatcher.dispatch_event(evt)

    def on_excellence(self):
        evt = DEvent("CONTROL_EXCELLENCE", {})
        dispatcher.dispatch_event(evt)

    def on_help(self):
        evt = DEvent("CONTROL_HELP", {})
        dispatcher.dispatch_event(evt)

    def on_about(self):
        evt = DEvent("CONTROL_ABOUT", {})
        dispatcher.dispatch_event(evt)

    def initialise_window(self):
        menu = Tkinter.Menu(self.root)
        self.root.config(menu=menu)

        #  File Menu -------- --------
        filemenu = Tkinter.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.on_new)
        filemenu.add_command(label="Open", command=self.on_open)
        filemenu.add_command(label="Save", command=self.on_save)
        filemenu.add_command(label="Save as", command=self.on_saveas)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_exit)

        #  Edit Menu -------- --------
        editmenu = Tkinter.Menu(menu)
        menu.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Undo", command=self.on_undo)
        editmenu.add_command(label="Redo", command=self.on_redo)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.on_cut)
        editmenu.add_command(label="Copy", command=self.on_copy)
        editmenu.add_command(label="Paste", command=self.on_paste)
        editmenu.add_command(label="Delete", command=self.on_delete)
        editmenu.add_separator()
        editmenu.add_command(label="Find", command=self.on_find)
        editmenu.add_command(label="Find next", command=self.on_findnext)
        editmenu.add_separator()
        editmenu.add_command(label="Select all", command=self.on_selectall)

        #  Options Menu -------- --------
        optionmenu = Tkinter.Menu(menu)
        menu.add_cascade(label="Options", menu=optionmenu)
        optionmenu.add_command(label="Preferences", command=self.on_preferences)
        optionmenu.add_command(label="Excellence", command=self.on_excellence)

        #  Help Menu -------- --------
        helpmenu = Tkinter.Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="View help", command=self.on_help)
        helpmenu.add_command(label="About", command=self.on_about)

        # Notebook (tabs) -------- --------
        self.nb = ttk.Notebook(self.root)
        #page1 = ttk.Frame(nb)


        # second page
        #page2 = NewHexViewer(nb, "data_set")

        #page3 = ttk.Frame(nb)

        #nb.add(page2, text='Hex')
        #nb.add(page1, text='ASCII')
        #nb.add(page3, text='Disassemble')
        self.nb.pack(expand=1, fill="both")

    def add_tab(self, frame):
        self.nb.add(frame, text=frame.title)
        self.nb.pack(expand=1, fill="both")
