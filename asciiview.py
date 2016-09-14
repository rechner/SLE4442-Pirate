from Tkinter import *   # basic Tkinter
#from tkFont import *
from dispatcher import dispatcher, DEvent
import re

DEFAULT_FONT = ("Courier", 14)

class ASCIIViewControl(object):
    view = None

    def __init__(self, root_control):
        self.root_control = root_control  # This points back to main app
        dispatcher.add_event_listener("LOAD_DATASET", self.on_load_dataset)
        dispatcher.add_event_listener("UPDATE_DATASET", self.on_update_dataset)

    def initialise(self):
        self.view = ASCIIViewer()
        self.root_control.view.add_tab(self.view)

    def on_load_dataset(self, event):
        self.view.set_data(event.data["dataset"])

    def on_update_dataset(self, event):
        self.view.redraw()


class ASCIIViewer(Frame):
    """ Show a data string as ascii.. like notepad
    """
    title = "ASCII"

    def __init__(self, master=None, data_set=None):
        # Initialize superclass
        Frame.__init__(self, master)

        self.dataset = data_set  # Dataset to display
        self.ascii_text = ASCIIText(master=self, state="normal", font=DEFAULT_FONT)
        self.ascii_text.pack(padx=5, pady=10, side=LEFT)

    def set_data(self, dataset):
        """ Set data in the frame
        """
        self.dataset = dataset
        self.redraw()

    def clear_data(self):
        """ Clears the data in the frame
        """
        self.ascii_text.clear()

    def remove_tag(self, offset, length, type, tag):
        """ Clear a tag at given offset """
        if self.dataset is None:
            return
        #self.ascii_text.remove_tag(offset, length, tag)

    def add_tag(self, offset, length, type, tag):
        if self.dataset is None:
            return

        #self.ascii_text.add_tag(offset, length, tag)

    def redraw(self):
        self.ascii_text.redraw()


class ASCIIText(Text):
    """ Display the data set as ascii printable characters, or a '.' if not printable
    so clover that my app has two classes with the same name.... """

    def __init__(self, *args, **kwargs):
        #super(HexText, self).__init__(*args, **kwargs)
        Text.__init__(self, *args, **kwargs)
        self.redraw()
        #self.bind("<Motion>", self.on_mousemotion)
        #self.bind("<ButtonPress-1>", self.on_mouseclick)
        #self.bind("<KeyPress>", self.on_keypress)  # Does not seem to work on linux?

        #self.bind("<<Copy>>", self.copy)
        #self.bind("<<Cut>>", self.cut)
        #self.bind("<<Paste>>", killEvent)
        #self.bind("<<Paste-Selection>>", killEvent)
        #self.bind("<<Clear>>", killEvent)
        #self.bind("<Key>", killEvent)

    def copy(self, evt):
        content = self.selection_get()
        print("CCOOPPYY", content)
        print "selected text: '%s'" % self.get(SEL_FIRST, SEL_LAST)
        print "three", self.index(SEL_FIRST), self.index(SEL_LAST)
        return "break"

    def cut(self, evt):
        print("CCCUTTT")
        return "break"

    def clear(self):
        self.configure(state="normal")
        self.delete("0.0", END)
        self.configure(state="normal")

    def redraw(self):
        """
        Clear and redraw the entire frame
        """
        dataset = self.master.dataset
        if dataset is None:
            return

        # ---
        self.clear()
        self.configure(state="normal")
        tag = ()  # Default tag to apply
        self.insert(END, dataset.data, tag)
        self.configure(state="disabled")