#!/usr/bin/python3

"""
Ugly GUI launcher
"""

try:
    import Tkinter as tk
except:
    import tkinter as tk

class GUI(object):
    def __init__(self, style = 'grid'):
        self.style = style
        self.window = tk.Tk()
        self.window.title('checkMate')
        self.selected = tk.IntVar()
        ourLst = [('ckl2csv',      0, 0, 0),
                  ('cklMod',       0, 1, 1),
                  ('cklVitals',    0, 2, 2),
                  ('rpmCompare',   0, 3, 3),
                  ('scapChecks',   0, 4, 4),
                  ('tempDrop',     0, 5, 5),
                  ('update',       0, 6, 6)]
        for k, col, row, v in ourLst:
            if self.style == 'pack':
                b = tk.Radiobutton(self.window, indicatoron = 0, text = k, variable = self.selected, value = v).pack(anchor = 'w')
            else:
                b = tk.Radiobutton(self.window, indicatoron = 0, text = k, variable = self.selected, value = v).grid(column = col, row = row)

    def clicked(self):
        """Action to take when clicked"""
        print(self.selected.get())

if __name__ == '__main__':
    g = GUI(style = 'pack')
    g.window.geometry('500x400')
    g.window.configure(background = 'mint cream')

    ## Add button not in the loop
    padY = 300
    if g.style == 'pack':
        btn = tk.Button(g.window, text = "Click Me", command = g.clicked).pack(anchor = 'e', pady = padY, side = 'bottom')
    else:
        btn = tk.Button(g.window, text = "Click Me", command = g.clicked).grid(column = 6, row = 9, pady = padY)

    ## loop
    g.window.mainloop()
