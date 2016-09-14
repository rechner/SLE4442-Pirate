from Tkinter import *   # basic Tkinter
#from tkFont import *
from dispatcher import dispatcher, DEvent
import re


#ROW_COUNT = 16  # rows
#COL_COUNT = 16  # columns
#HEX_OFFSET = 10
#ASCII_OFFSET = 59

INPUT_OFF = 0
INPUT_ON = 1

SELECT_NONE = 0x0
SELECT_ASCII = 0x1
SELECT_HEX = 0x2
SELECT_ADDRESS = 0x4
SELECT_ALL = 0x7

FIRST_CHAR = 1
SECOND_CHAR = 2

DEFAULT_FONT = ("Courier", 14)

ASCII_HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']

def killEvent(evt):
    return "break"


class HexViewControl(object):
    def __init__(self, root_control):
        self.root_control = root_control  # This points back to main app
        dispatcher.add_event_listener("LOAD_DATASET", self.on_load_dataset)
        dispatcher.add_event_listener("UPDATE_DATASET", self.on_update_dataset)

    def initialise(self):
        self.view = HexViewer()
        self.root_control.view.add_tab(self.view)

    def on_load_dataset(self, event):
        self.view.set_data(event.data["dataset"])

    def on_update_dataset(self, event):
        self.view.redraw()


class HexViewer(Frame):
    """ Show a data string as hex digits, editable!
    """
    title = "Hex"
    def __init__(self, master=None, data_set=None):
        # Initialize superclass
        Frame.__init__(self, master)

        self.byte_width = 2  # Number of bytes to display per row
        self.dataset = data_set  # Dataset to display

        self.hex_input_progress = FIRST_CHAR  # Progress of entering hex (first or second octet)
        self.hex_input_byte = 0  # Hold octet temporarily
        #self.current_highlight = 0  # currently highlighted offset
        self.current_selection_off = 0  # Currently selected offset typle, (selection_offset, selection_length)
        self.current_selection_len = 1  # Number of bytes selected (can be negative)
        self.current_select_type = SELECT_NONE  # Ascii or hex selected
        self.current_hover = 0  # Current offset which is being hovered over
        self.char_height = 52  # number of rows to show

        self.address_text = AddressText(master=self, state="normal", font=DEFAULT_FONT)
        self.address_text.pack(padx=5, pady=10, side=LEFT)
        self.hex_text = HexText(master=self, state="normal", font=DEFAULT_FONT)
        self.hex_text.pack(padx=5, pady=10, side=LEFT)
        self.ascii_text = ASCIIText(master=self, state="normal", font=DEFAULT_FONT)
        self.ascii_text.pack(padx=5, pady=10, side=LEFT)

        self.hex_text.delete("0.0", END)
        self.hex_text.tag_config("selected", background="light blue", underline=1)
        self.hex_text.tag_config("shadowed", background="red")
        self.hex_text.tag_config("hover", background="gray")

        self.ascii_text.delete("0.0", END)
        self.ascii_text.tag_config("selected", background="light blue", underline=1)
        self.ascii_text.tag_config("shadowed", background="red")
        self.ascii_text.tag_config("hover", background="gray")

        #self.bind("<KeyPress>", self.on_keypress)  # Does not seem to work on linux?
        #self.text = Text(master=self, state="normal", font=DEFAULT_FONT)
        #self.hex_text.bind("<KeyPress>", self.keypress)  # Does not seem to work on linux?
        #self.bind("<KeyPress>", self.on_keypress)  # Does not seem to work on linux?

        #self.text.pack()

        #self.text.delete("0.0", END)
        #self.text.tag_config("selected", underline=1)
        #self.text.tag_config("shadowed", background="red")
        #self.text.tag_config("hover", background="gray")

    def change_byte_width(self, new_width):
        if new_width % 8 != 0:
            raise Exception("byte width must be multiple of 8")
        self.byte_width = new_width

    def set_hover(self, offset):
        """ Set the current element being hovered over"""
        self.remove_tag(self.current_hover, 1, SELECT_ALL, "hover")
        self.current_hover = offset
        self.add_tag(offset, 1, SELECT_ALL, "hover")

    def set_selected(self, offset, length, type):
        """ Set the current selected text """
        self.remove_tag(self.current_selection_off, 1, SELECT_ALL, "selected")
        self.current_selection_off = offset
        self.current_select_type = type
        self.add_tag(offset, length, type, "selected")

    def set_data(self, dataset):
        """ Set data in the frame
        """
        self.dataset = dataset
        self.redraw()

    def clear_data(self):
        """ Clears the data in the frame
        """
        self.address_text.clear()
        self.hex_text.clear()
        self.ascii_text.clear()

        self.address_text.configure(state="normal")
        self.address_text.delete("0.0", END)
        self.address_text.configure(state="disabled")

        self.hex_text.configure(state="normal")
        self.hex_text.delete("0.0", END)
        self.hex_text.configure(state="disabled")

        self.ascii_text.configure(state="normal")
        self.ascii_text.delete("0.0", END)
        self.ascii_text.configure(state="disabled")

    def remove_tag(self, offset, length, type, tag):
        """ Clear a tag at given offset """
        if self.dataset is None:
            return

        if offset > len(self.dataset.data):
            return
        if type & SELECT_ASCII > 0:
            self.ascii_text.remove_tag(offset, length, tag)
        if type & SELECT_HEX > 0:
            self.hex_text.remove_tag(offset, length, tag)

    def add_tag(self, offset, length, type, tag):
        """ Apply a tag to a particular character(s)
        type is a bit mask which determins which text field to apply to, including
         SELECT_ASCII, SELECT_HEX, SELECT_OFFSET"""
        if self.dataset is None:
            return

        if offset > len(self.dataset.data):
            return
        if type & SELECT_ASCII > 0:
            self.ascii_text.add_tag(offset, length, tag)
        if type & SELECT_HEX > 0:
            self.hex_text.add_tag(offset, length, tag)

    def update_textfield(self, textfield, position, data):
        """ Update the text field object with the data specified at the position specified
        """
        pass

    def redraw(self):
        """ Update the character of position offset """
        self.address_text.redraw()
        self.ascii_text.redraw()
        self.hex_text.redraw()

    def on_keypress(self, event):
        """ Callback on a key press event.
        """
        if self.current_select_type == SELECT_ASCII:
            offset = self.current_selection_off
            self.dataset.insert(offset, event.char)
            self.set_selected(self.current_selection_off + 1, 1, self.current_select_type)
            self.redraw()
        elif self.current_select_type == SELECT_HEX:
            offset = self.current_selection_off
            if event.keysym not in ASCII_HEX:
                print "non ascii char entered"
                return
            evali = 0
            evalmsk = 0
            #self.hex_input_byte
            if self.hex_input_progress == FIRST_CHAR:
                self.hex_input_byte = int(event.keysym, 16) << 4
                self.hex_input_progress = SECOND_CHAR
            elif self.hex_input_progress == SECOND_CHAR:
                #evali = int(event.keysym, 16)
                self.hex_input_byte = self.hex_input_byte | int(event.keysym, 16)
                ins = bytearray(1)
                ins[0] = self.hex_input_byte
                print("INSERT:", bytearray(self.hex_input_byte), len(bytearray(self.hex_input_byte)))
                self.dataset.insert(offset, ins)
                #evalmsk = int('F0', 16)
                self.set_selected(self.current_selection_off + 1, 1, self.current_select_type)
                self.redraw()
                self.hex_input_progress = FIRST_CHAR

            # for over-writing mode???????
            #result = int((self.dataset[offset] & evalmsk) | evali)
            #self.dataset.insert(offset, result)
                #self.redraw()


class ASCIIText(Text):
    """ Display the data set as ascii printable characters, or a '.' if not printable"""
    byte_width = 8
    frame_width = 9

    def __init__(self, *args, **kwargs):
        #super(HexText, self).__init__(*args, **kwargs)
        Text.__init__(self, *args, **kwargs)
        self.redraw(0)
        self.bind("<Motion>", self.on_mousemotion)
        self.bind("<ButtonPress-1>", self.on_mouseclick)
        self.bind("<KeyPress>", self.on_keypress)  # Does not seem to work on linux?

        self.bind("<<Copy>>", self.copy)
        self.bind("<<Cut>>", self.cut)
        self.bind("<<Paste>>", killEvent)
        self.bind("<<Paste-Selection>>", killEvent)
        self.bind("<<Clear>>", killEvent)
        self.bind("<Key>", killEvent)

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
        self.configure(state="disabled")

    def redraw(self, offset=None):
        """
        Clear and redraw the entire frame
        """
        self.byte_width = self.master.byte_width
        self.frame_width = self.byte_width * 8 + (self.byte_width -1)
        self.frame_height = self.master.char_height
        self.width = self.frame_width
        self.config(width=self.frame_width, height=self.frame_height)
        dataset = self.master.dataset
        if dataset is None:
            return

        # ---
        self.clear()
        self.configure(state="normal")
        self.width = self.frame_width

        tag = ()  # Default tag to apply

        for rownumber in range(0, self.frame_height):
            for columnnumber in range(0, (self.byte_width*8)):
                offset = rownumber*(self.byte_width*8) + columnnumber
                if offset >= len(dataset.data):
                    return
                char = chr(dataset.data[offset])

                if ord(char) < 32 or ord(char) > 126:
                    self.insert(END, ".", tag)
                else:
                    self.insert(END, char, tag)
                if columnnumber % 8 == 7 and columnnumber != self.byte_width*8-1:
                    self.insert(END, " ", tag)  # This adds white liens between bytes

            self.insert(END, "\n", tag)

        self.configure(state="disabled")

    def pcoord_to_offset(self, x, y):
        coordIndex = "@%d,%d" % (x, y)
        charIndex = self.index(coordIndex)
        row, col = int(charIndex.split('.')[0]), int(charIndex.split('.')[1])
        # Now we have row and column of the click....
        row_offset = (row-1) * self.byte_width * 8  # row -1 because columns start at 1 (instead of 0)
        col_offset = col
        col_special = (col / 8) * 1  # This account for the extra white lines between 8 bytes
        ret = row_offset + (col_offset - col_special)
        return row_offset + (col_offset - col_special)

    def offset_to_coord(self, offset):
        row = offset / (self.byte_width*8) + 1
        col = offset % (self.byte_width*8)
        col_special = (col / 8)
        asciicoord = (col + col_special, row)
        return asciicoord

    def remove_tag(self, offset, length, tag):
        """ Clear a tag at given offset """
        dataset = self.master.dataset
        if dataset is None:
            return

        col, row = self.offset_to_coord(offset)
        index = "%d.%d" % (row, col)  # row column weird tkinter
        self.tag_remove(tag, index, index + " + 1 chars")

    def add_tag(self, offset, length, tag):
        """ Apply a tag to a particular character(s)
        type is a bit mask which determins which text field to apply to, including
         SELECT_ASCII, SELECT_HEX, SELECT_OFFSET"""
        dataset = self.master.dataset
        if dataset is None:
            return

        col, row = self.offset_to_coord(offset)
        index = "%d.%d" % (row, col)  # row column weird tkinter
        self.tag_add(tag, index, index + " + 1 chars")

    def on_mouseclick(self, event):
        coordIndex = "@%d,%d" % (event.x, event.y)
        charIndex = self.index(coordIndex)
        col, row = int(charIndex.split('.')[0]), int(charIndex.split('.')[1])
        offset = self.pcoord_to_offset(event.x, event.y)

        self.master.set_selected(offset, 1, SELECT_ASCII)

    def on_mousemotion(self, event):
        offset = self.pcoord_to_offset(event.x, event.y)
        if offset is None:
            return

        self.master.set_hover(offset)

    def on_keypress(self, event):
        """ Callback on a key press event.
        """
        #offset = self.current_select
        print("ascii keypress:", event.keysym)
        self.master.on_keypress(event)


class HexText(Text):
    byte_width = 8

    def __init__(self, *args, **kwargs):
        #super(HexText, self).__init__(*args, **kwargs)
        Text.__init__(self, *args, **kwargs)
        self.redraw(0)
        self.bind("<Motion>", self.on_mousemotion)
        self.bind("<ButtonPress-1>", self.on_mouseclick)
        self.bind("<KeyPress>", self.on_keypress)  # Does not seem to work on linux?

    def clear(self):
        self.configure(state="normal")
        self.delete("0.0", END)
        self.configure(state="disabled")

    def redraw(self, offset=None):
        """
        Clear and redraw the entire frame
        """
        self.byte_width = self.master.byte_width
        self.frame_width = self.byte_width * 8 * 3 + (self.byte_width -1)
        self.frame_height = self.master.char_height
        self.config(width=self.frame_width, height=self.frame_height)
        dataset = self.master.dataset
        if dataset is None:
            return

        # ---
        self.clear()
        self.configure(state="normal")
        self.width = self.frame_width

        tag = ()  # Default tag to apply

        for rownumber in range(0, self.frame_height):
            for columnnumber in range(0, (self.byte_width * 8)):
                offset = rownumber * (self.byte_width * 8) + columnnumber
                if offset >= len(dataset.data):
                    return
                text = "{0:02x}".format(dataset.data[offset])
                self.insert(END, text, tag)
                if columnnumber % 8 == 7:
                    self.insert(END, " ", tag)  # This adds white liens between bytes
                if columnnumber != self.byte_width * 8 - 1:
                    self.insert(END, " ", tag)

            self.insert(END, "\n", tag)

        self.configure(state="disabled")

    def pcoord_to_offset(self, x, y):
        """ convert x,y pixel coordinates (offset from the frames top left corner) within the hex frame into an offset
        (offset being the offset of the byte from the start of the dataset) """
        dataset = self.master.dataset
        if dataset is None:
            return None

        coordIndex = "@%d,%d" % (x, y)  # Convert to tkinter Text coords
        charIndex = self.index(coordIndex)
        row, col = int(charIndex.split('.')[0]), int(charIndex.split('.')[1])
        # Now we have row and column of the click.... resolve to an offset
        row_offset = (row - 1) * self.byte_width * 8  # row -1 because columns start at 1 (instead of 0)
        col_offset = col
        col_special = (col + 1) / 3  # This accounts for white space between bytes
        col_special += col / 24  # This account for the extra white lines between sets of 8 bytes
        return row_offset + (col_offset - col_special) / 2

    def offset_to_coord(self, offset):
        """ Convert an offset (as in offset from the start of the dataset) integer into column,row tuple """
        row = offset / (self.byte_width * 8) + 1
        col = (offset % (self.byte_width * 8)) * 3
        col_special = (col / 23)
        hexcoord = (col + col_special, row)
        return hexcoord

    def remove_tag(self, offset, length, tag):
        """ Clear a tag at given offset """
        dataset = self.master.dataset
        if dataset is None:
            return

        col, row = self.offset_to_coord(offset)
        index = "%d.%d" % (row, col)  # row column weird tkinter
        self.tag_remove(tag, index, index + " + 2 chars")

    def add_tag(self, offset, length, tag):
        """ Apply a tag to a particular character(s)
        type is a bit mask which determins which text field to apply to, including
         SELECT_ASCII, SELECT_HEX, SELECT_OFFSET"""
        dataset = self.master.dataset
        if dataset is None:
            return

        col, row = self.offset_to_coord(offset)
        index = "%d.%d" % (row, col)  # row column weird tkinter
        self.tag_add(tag, index, index + " + 2 chars")

    def on_mouseclick(self, event):
        # offset, type = self.coord_to_offset(event.x, event.y)
        # if offset is not None:
        #    self.set_selected(offset, type)
        coordIndex = "@%d,%d" % (event.x, event.y)
        charIndex = self.index(coordIndex)
        col, row = int(charIndex.split('.')[0]), int(charIndex.split('.')[1])
        offset = self.pcoord_to_offset(event.x, event.y)

        self.master.set_selected(offset, 1, SELECT_HEX)

    def on_mousemotion(self, event):
        mousepos = "@%d,%d" % (event.x, event.y)
        # print "mousepos: %s character: %s" % (mousepos, self.text.get(mousepos))
        # print "ERINFO", event, self, event.x, event.y
        offset = self.pcoord_to_offset(event.x, event.y)
        if offset is None:
            return

        self.master.set_hover(offset)

    def on_keypress(self, event):
        """ Callback on a key press event.
        """
        #offset = self.current_select
        print("hex keypress:", event.keysym)
        self.master.on_keypress(event)

        # move selected to next character
        #self.set_selected(self.current_select + 1, self.current_select_type)
        #elif self.current_select_type == SELECT_HEX:
        #offset = self.current_select
        #if event.keysym not in ASCII_HEX:
        #    print "non ascii char entered"
        #    return

        #evali = 0
        #evalmsk = 0
        #if self.ascii_enter_progress == FIRST_CHAR:
        #    evali = int(event.keysym, 16) << 4
        #    evalmsk = int('0F', 16)
        #    self.ascii_enter_progress = SECOND_CHAR
        #elif self.ascii_enter_progress == SECOND_CHAR:
        #    evali = int(event.keysym, 16)
        #    evalmsk = int('F0', 16)
        #    self.ascii_enter_progress = FIRST_CHAR
        #    self.set_selected(self.current_select + 1, self.current_select_type)

        #result = int((self.dataset[offset] & evalmsk) | evali)
        #self.dataset[offset] = result
        #self.update_display(offset)


class AddressText(Text):
    byte_width = 8

    def __init__(self, *args, **kwargs):
        # super(HexText, self).__init__(*args, **kwargs)
        Text.__init__(self, *args, **kwargs)
        self.redraw(0)
        self.bind("<Motion>", self.on_mousemotion)
        self.bind("<ButtonPress-1>", self.on_mouseclick)

    def clear(self):
        self.configure(state="normal")
        self.delete("0.0", END)
        self.configure(state="disabled")

    def redraw(self, offset=None):
        """
        Update the address text (left side frame)
        """
        self.byte_width = self.master.byte_width
        self.frame_width = 10
        self.frame_height = self.master.char_height
        self.config(width=self.frame_width, height=self.frame_height)
        dataset = self.master.dataset
        if dataset is None:
            return

        self.configure(state="normal")

        for row in range(0, self.frame_height):
            text = "0x{0:08x}".format(row * self.byte_width)
            self.insert(END, text + "\n")

        self.configure(state="disabled")

    def pcoord_to_offset(self, x, y):
        coordIndex = "@%d,%d" % (x, y)
        charIndex = self.index(coordIndex)
        row, col = int(charIndex.split('.')[0]), int(charIndex.split('.')[1])
        # Now we have row and column of the click....
        row_offset = (row-1) * self.byte_width * 8  # row -1 because columns start at 1 (instead of 0)
        col_offset = col
        col_special = (col / 8) * 1  # This account for the extra white lines between 8 bytes
        ret = row_offset + (col_offset - col_special)
        return row_offset + (col_offset - col_special)

    def offset_to_coord(self, offset):
        row = offset / (self.byte_width*8) + 1
        col = offset % (self.byte_width*8)
        col_special = (col / 8)
        asciicoord = (col + col_special, row)
        return asciicoord

    def on_mouseclick(self, event):
        pass
        coordIndex = "@%d,%d" % (event.x, event.y)
        charIndex = self.index(coordIndex)
        col, row = int(charIndex.split('.')[0]), int(charIndex.split('.')[1])
        offset = self.pcoord_to_offset(event.x, event.y)

        self.master.set_selected(offset, 1, SELECT_ALL)

    def on_mousemotion(self, event):
        pass

        mousepos = "@%d,%d" % (event.x, event.y)
        # print "mousepos: %s character: %s" % (mousepos, self.text.get(mousepos))
        # print "ERINFO", event, self, event.x, event.y
        offset = self.pcoord_to_offset(event.x, event.y)
        if offset is None:
            return

        self.master.set_hover(offset)