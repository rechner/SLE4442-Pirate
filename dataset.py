""" I believe this incorporates the command patterd from design patterns book """

TEXT_MODE_OVERTYPE = 1
TEXT_MODE_INSERT = 2


class Command(object):
    """ This is an abstract class which represents a action and transformation performed on a dataset.
        This includes the execute method, which performs the transaction, and the unexecute method which reverses
        the transaction """
    def execute(self, dataset):
        pass

    def unexecute(self, dataset):
        pass


class InsertOperator(Command):
    def __init__(self, position, newdata):
        self.newdata = newdata
        self.position = position

    def execute(self, dataset):
        dataset.data = dataset.data[: self.position] + self.newdata + dataset.data[self.position:]

    def unexecute(self, dataset):
        dataset.data = dataset.data[: self.position] + dataset.data[self.position+len(self.newdata):]


class DeleteOperator(Command):
    def __init__(self, position, count):
        self.delcount = count
        self.position = position
        self.removed_data = ""

    def execute(self, dataset):
        self.removed_data = dataset.data[self.position: self.position + self.delcount]
        dataset.data = dataset.data[:self.position] + dataset.data[self.position + self.delcount:]

    def unexecute(self, dataset):
        dataset.data = dataset.data[:self.position] + self.removed_data + dataset.data[self.position:]


class OvertypeOperator(Command):
    def __init__(self, position, newdata):
        self.newdata = newdata
        self.position = position
        self.removed_data = ""

    def execute(self, dataset):
        self.removed_data = dataset.data[self.position: self.position + len(self.newdata)]
        dataset.data = dataset.data[: self.position] + self.newdata + dataset.data[self.position + len(self.newdata):]

    def unexecute(self, dataset):
        dataset.data = dataset.data[:self.position] + self.removed_data + dataset.data[self.position + len(self.newdata):]


class Dataset(object):
    """ A dataset represents a piece of data """
    data = bytearray("")  # use a simple string for now
    command_history = []  # a list of 'Command' that have been applied to the dataset
    command_offset = 0  # offset of the current Command
    #insert_mode = TEXT_MODE_INSERT

    def __init__(self, initial_data=None):
        if initial_data is not None:
            self.data = bytearray(initial_data)

    def read(self, start_offset, end_offset):
        return self.data[start_offset, end_offset]

    def insert(self, position, data):
        """ Insert data into the given position in the dataset. position is an offset from the start of the data """
        new_op = InsertOperator(position, data)
        new_op.execute(self)
        self.command_history.insert(self.command_offset, new_op)
        self.command_offset += 1

#    def _insert(self, position, newdata):
#        self.data = self.data[: position] + newdata + self.data[position:]
#
#    def _delete(self, position, count):
#        removed_data = self.data[position: position + count]
#        self.data[:position] + self.data[position + count:]
#        return removed_data

    def overtype(self, position, data):
        """ Insert data into the given position in the dataset, overwriting any data which is currently in that
            position.  is an offset from the start of the data """
        new_op = OvertypeOperator(position, data)
        new_op.execute(self)
        self.command_history.insert(self.command_offset, new_op)
        self.command_offset += 1

    def delete(self, position, count):
        """ remove count bytes starting at the given position """
        new_op = DeleteOperator(position, count)
        new_op.execute(self)
        self.command_history.insert(self.command_offset, new_op)
        self.command_offset += 1

    def undo(self):
        """ Undo the previous command from the command history """
        if self.command_offset == 0:
            return  # cannot undo past first command
        op = self.command_history[self.command_offset-1]
        op.unexecute(self)
        self.command_offset -= 1

    def redo(self):
        """ Redo the previous undone command from the command history """
        if self.command_offset == len(self.command_history):
            return  # cannot redo past most recent command
        op = self.command_history[self.command_offset]
        op.execute(self)
        self.command_offset += 1

