
from tkinter import *
from tkinter import filedialog
from coords_canvas_RT import Coords_canvas_RT
import pandas as pd
import os
from publication_resistance_RT import Publication_resistance_RT



class Main_Panel(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill = 'both', expand = True)
        self.f = Frame(self, width = 600, height = 100)
        import_b = Button(self, text = 'import data', fg = 'green',  command = self.on_import)



        self.f.grid(row = 0, column =0, columnspan = 2, sticky = 'news', padx = (5,5), pady = (3,3))
        import_b.grid(row = 1, column =0, padx = (5,5), sticky = 'se', pady = (3,3))

        # self.item = {}

    def on_OK(self, item):
        w = Toplevel(self)
        w.title(item['title'])
        Main_RT(w, item['data'])


    def on_import(self):
        filename =  filedialog.askopenfilename(title = "Select file")
        if len(filename) == 0: return
        filetype = os.path.splitext(filename)[1]
        if filetype == '.txt':
            d = pd.read_csv(filename, header = None, sep = '\t')
        elif filetype == '.csv':
            d = pd.read_csv(filename, header =1)
        else:
            return

        coords = [(x,y) for x, y in zip(d.iloc[:, 0], d.iloc[:,1])]
        resis = d.iloc[:, 2:5].mean(axis =1) # take average

        data = {k:v for k,v in zip(coords, resis)}
        item = {'title': filename, 'data':data}

        #add new item GUI
        item_l = LabelFrame(self.f, text = filename )
        Label(item_l, text = f'total MAs: {len(resis)}', fg = 'blue').pack()
        ok_b = Button(self.f, text = 'ok', fg = 'red', width = 6, command = lambda item=item: self.on_OK(item))
        item_l.pack()
        ok_b.pack(anchor = 'ne', pady = (1, 10))





class Main_RT(Coords_canvas_RT):
    def __init__(self, master, data):
        super().__init__(master)

        delete_b = Button(master, text = 'remove selected MA', fg = 'red', command = self.on_remove_selected)
        publication_b = Button(master, text = 'publication', fg = 'red', command = self.on_publication)

        self.pack( padx = (5,5), pady = (5,5), fill = 'both', expand = True)
        delete_b.pack(padx = (5,5), pady = (5,5))
        publication_b.pack(padx = (5,5), pady = (5,5))

        self.set_data(data)

    def on_publication(self):
        w = Toplevel(self)
        w.title('set figure for publicaiton')
        c, ax,fig, cbar, cax = self.get_para_fig()
        Publication_resistance_RT(w,  c, ax,fig, cbar, cax)

    def on_remove_selected(self):
        self.remove_and_update()




def main():
    root = Tk()
    Main_Panel(root)


    root.mainloop()

if __name__ == '__main__':
    main()
