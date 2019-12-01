import tkinter as tk


def CheckValueRange(value):
    if value not in range(1, 10):
        raise ValueError("value {val} not in valid range".format(val=value))

def GetBlock(row, col):
    return (row // 3) * 3 + (col // 3)

class SudokuException(Exception):
    pass

class SudokuBlock():
    def __init__(self, row, col, setValue=None):
        if setValue is None:
            self._possibleValues = set(range(1, 10))
        else:
            CheckValueRange(setValue)
            self._possibleValues = set([setValue])

        self._stringVars = row
        self._col = col
        self._row = row
        self._block = GetBlock(row, col)

        # The callbacks are called once a value is fixed.
        self._callBackFunctions = []

        self._isInit = False

    def init(self, value):
        self._isInit = True
        self.setValue(value)
    
    def setValue(self, value):
        CheckValueRange(value)
        self._possibleValues = set([value])
        self._runCallBacks()
    
    def getValues(self):
        values = list(self._possibleValues)
        values.sort()
        return values

    def getRow(self):
        return self._row

    def getCol(self):
        return self._col

    def getBlock(self):
        return self._block

    def isInit(self):
        return self._isInit
    
    def removeValue(self, value):
        
        if len(self._possibleValues) == 1 and value in self._possibleValues:
            raise SudokuException("It is not allowed to remove the last number ({num}) from square.".format(num=value))
        if value in self._possibleValues:
            self._possibleValues.remove(value)
            if len(self._possibleValues) == 1:
                self._runCallBacks()

    def registerCallback(self, newCbFun):
        self._callBackFunctions.append(newCbFun)
    
    def callBack(self, other):
        if self._row == other.getRow() or self._col == other.getCol() or self._block == other.getBlock():
            otherValues = other.getValues()
            if len(otherValues) > 1:
                raise SudokuException("len(otherValues) expected to equal 1.")
            self.removeValue(other.getValues()[0])
    
    def _runCallBacks(self):
        for cb in self._callBackFunctions:
            cb(self)
    
    def __str__(self):
        values = list(self._possibleValues)
        values.sort()
        return "row={row}, col={col}, block={block}, values={values}".format(row=self._row, col=self._col, block=self._block, values=values)


class Sudoku():
    def __init__(self):
        super().__init__()

        self._grid = []
        for row in range(9):
            self._grid.append([])
            for col in range(9):
                self._grid[row].append(SudokuBlock(row, col))

        for first in self._iterateAllCells():
            for second in self._iterateAllCells():
                if not first == second:
                    first.registerCallback(second.callBack)


    def _iterateAllCells(self):
        for row in self._grid:
            for col in row:
                yield col
        

    def init(self, row, col, value):
        CheckValueRange(value)
        self._grid[row][col].init(value)

    def setValue(self, row, col, value):
        CheckValueRange(value)
        self._grid[row][col].setValue(value)

    def getValues(self, row, col):
        return self._grid[row][col].getValues()

    def isInit(self, row, col):
        return self._grid[row][col].isInit()




class InputSquares(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self._init = True

        def getColor(count):
            if count % 2 == 0:
                return "PaleGreen1"
            return "DarkOliveGreen"


        self._stringVars = []
        self._entries = []
        for row in range(9):
            self._stringVars.append([])
            self._entries.append([])
            for col in range(9):
                stringVar = tk.StringVar()
                self._stringVars[row].append(stringVar)

        count=0
        self._blocks = []
        for i in range(3):
            for j in range(3):
                count += 1
                subFrame = tk.Frame(self, background=getColor(count))
                for k in range(3):
                    for l in range(3):
                        row = i * 3 + k
                        col = j * 3 + l
                        entry = tk.Entry(subFrame, textvariable=self._stringVars[row][col], width=2, font="Helvetica 44 bold")
                        entry.grid(row=k, column=l, padx=3, pady=3)
                        self._entries[row].append(entry)
                subFrame.grid(row=i, column=j)
        
        self._button = tk.Button(self, text="Start", command=self._start)
        self._button.grid(row=10, column=0, columnspan=3)

        self._sudoku = Sudoku()


    def _start(self):
        print("Start")

        for row in range(9):
            for col in range(9):
                stringValue = self._stringVars[row][col].get()
                if stringValue != "":
                    try:
                        value = int(stringValue)
                        if value in range(1, 10):
                            if self._init:
                                self._sudoku.init(row, col, value)
                            elif not self._sudoku.isInit(row, col):
                                self._sudoku.setValue(row, col, value)
                    except ValueError:
                        pass

        self._init = False
        self._button.configure(text="Continue")
        self._update()
        
    def _update(self):
        for row in range(9):
            for col in range(9):
                stringVar = self._stringVars[row][col]
                values = self._sudoku.getValues(row, col)
                if len(values) == 1:
                    stringVar.set(str(values[0]))
                    if self._sudoku.isInit(row, col):
                        self._entries[row][col].config(fg="red")
                    else:
                        self._entries[row][col].config(fg="SpringGreen4")
                else:
                    stringVar.set("[{len}]".format(len=len(values)))
                    self._entries[row][col].config(fg="old lace")





if __name__ == "__main__":
    root = tk.Tk()

    app = InputSquares(root).grid(row=0, column=0)
    #label = tk.Label(root, text="sldkfjls").grid(row=0, column=0)
    #label = tk.Label(root, text="dflkd").grid(row=1, column=0)

    root.mainloop()