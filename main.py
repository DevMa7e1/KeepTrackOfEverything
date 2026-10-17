import ttkbootstrap as ttk
from ttkbootstrap.dialogs import filedialog
from ktoe_classes import *
import dill
from tkinter.font import Font

root = ttk.App(title='KeepTrackOfEverything')
root.theme_use('bootstrap-dark')

the_frame = ttk.Frame(root)
tree: Location

def tree_view(name: str | ttk.Entry, window = None):
    if type(name) == ttk.Entry:
        name = name.get()
    global root, the_frame, tree
    tree = Location(name, the_frame) #type: ignore
    ttk.Button(root, text=tree.name, command=tree.click, bootstyle='primary').pack()
    the_frame.pack()
    if window != None:
        window.destroy()

def new_tree_view():
    window = ttk.Toplevel(title='New diagram')
    window.resizable(width=False, height=False)
    ttk.Label(window, text='Name:', justify='left').pack(fill='x', expand=True, padx=(0, 4))
    name = ttk.Entry(window).pack(padx=(0, 4), pady=4)
    ttk.Button(window, text='Add', command=partial(tree_view, name, window), bootstyle='primary').pack(padx=4, pady=4)

def search_tree(query: str):
    global tree
    all_elements = []
    actual_elements = []
    places: list[Place] = []
    places2: list[Place] = []
    for i in tree.children:
        if type(i) == Place:
            places2.append(i)
        all_elements.append(i.name)
        actual_elements.append(i)
    
    while len(places2) != 0:
        places = places2
        places2 = []
        for place in places:
            for i in place.children:
                if type(i) == Place:
                    places2.append(i)
                all_elements.append(i.name)
                actual_elements.append(i)
    window = ttk.Toplevel(title='Search result')
    frame = ttk.Frame(window)
    found = []
    for i in range(len(all_elements)):
        if query.lower() in all_elements[i].lower():
            found.append(actual_elements[i])

    newtree = BasicTree(tree)
    namestree = BasicTree(tree)
    for i in found:
        chain = [i]
        thing = i
        while type(thing.location) != Location:
            chain.append(thing.location)
            thing = thing.location
        curdict = newtree
        curdictname = namestree
        for i in range(len(chain)-1, 0-1, -1):
            if chain[i] in curdict:
                curdict = curdict[chain[i]]
                curdictname = curdictname[chain[i].name]
            else:
                curdict[chain[i]] = BasicTree(chain[i])
                curdict = curdict[chain[i]]
                curdictname[chain[i].name] = BasicTree(chain[i])
                curdictname = curdictname[chain[i].name]
    frame.pack()
    construct_tree(newtree, frame)

def construct_tree(basic: BasicTree, frame: ttk.Frame):
    places: list[BasicTree] = []
    places2: list[BasicTree] = []
    frames = {}
    for i in basic.children():
        if i not in frames.keys():
            frames[i] = [ttk.Frame(frame, relief='solid', borderwidth=1).grid(row=2, column=len(frames.keys()), padx=4, pady=(0, 4), sticky='n'), 0]
        ttk.Button(frame, text=i.name, bootstyle='success').grid(row=1, column=len(frames.keys())-1, padx=4, pady=(4, 0))
        places2.append(basic[i])
    while len(places2) != 0:
        places = places2
        places2 = []
        for place in places:
            for i in place.children():
                if type(i) == Place:
                    places2.append(place[i])
                    frames[i] = [ttk.Frame(frames[place.owner()][0], relief='solid', borderwidth=1).grid(row=2, column=frames[place.owner()][1], padx=4, pady=(0, 4), sticky='n'), 0]
                    ttk.Button(frames[place.owner()][0], text=i.name, bootstyle='warning').grid(row=1, column=frames[place.owner()][1], padx=4, pady=(4, 0))
                else:
                    ttk.Button(frames[place.owner()][0], text=i.name, bootstyle='secondary').grid(row=1, column=frames[place.owner()][1], padx=4, pady=(4, 4))
                frames[place.owner()][1] += 1

def deconstruct_tree():
    places: list[Place] = []
    places2: list[Place] = []
    for i in tree.children:
        if type(i) == Place:
            places2.append(i)
            i.frames = []
        i.root = None
    
    while len(places2) != 0:
        places = places2
        places2 = []
        for place in places:
            for i in place.children:
                if type(i) == Place:
                    places2.append(i)
                    i.frames = []
                i.root = None #type: ignore
    tree.root = None #type: ignore
    tree.frames = []
    save_tree(dill.dumps(tree))
    root.destroy()

def save_tree(dump: bytes):
    fd = filedialog.FileDialog(root, mode=filedialog.SAVE, title='Save diagram', filetypes=[('KeepTrackOfEverything diagram', '.ktoe')])
    fd.show()
    if fd.result != None:
        if fd.result[len(fd.result)-5:] != '.ktoe': 
            f = open(fd.result+'.ktoe', 'wb') #type: ignore
        else:
            f = open(fd.result, 'wb') #type: ignore
        f.write(dump)
        f.close()

def load_tree():
    fd = filedialog.FileDialog(root, title='Open a diagram', filetypes=[('KeepTrackOfEverything diagram', '.ktoe')])
    fd.show()
    if fd.result != None:
        f = open(fd.result, 'rb') #type: ignore
        dump = f.read()
        return dump

def reconstruct_tree():
    global tree
    dump = load_tree()
    tree = dill.loads(dump)
    tree_view(tree.name)
    frames = {}
    places = []
    places2 = []
    for i in tree.children:
        if i not in frames.keys():
            frames[i] = [ttk.Frame(the_frame, relief='solid', borderwidth=1).grid(row=2, column=len(frames.keys()), padx=4, pady=(0, 4), sticky='n'), 0]
        ttk.Button(the_frame, text=i.name, bootstyle='success', command=i.click).grid(row=1, column=len(frames.keys())-1, padx=4, pady=(4, 0))
        i.root = frames[i][0]
        tree.frames.append(frames[i])
        places2.append(i)
    while len(places2) != 0:
        places = places2
        places2 = []
        for place in places:
            for i in place.children:
                if type(i) == Place:
                    places2.append(i)
                    frames[i] = [ttk.Frame(frames[place][0], relief='solid', borderwidth=1).grid(row=2, column=frames[place][1], padx=4, pady=(0, 4), sticky='n'), 0]
                    i.root = frames[i][0]
                    place.frames.append(frames[i])
                    ttk.Button(frames[place][0], text=i.name, bootstyle='warning', command=i.click).grid(row=1, column=frames[place][1], padx=4, pady=(4, 0))
                else:
                    ttk.Button(frames[place][0], text=i.name, bootstyle='secondary').grid(row=1, column=frames[place][1], padx=4, pady=(4, 4))
                frames[place][1] += 1

menu_bar = ttk.Menu(root)
root.config(menu=menu_bar)

file_menu = ttk.Menu(menu_bar)
file_menu.add_command(label='Load diagram', command=reconstruct_tree)
file_menu.add_command(label='Save diagram', command=deconstruct_tree)
menu_bar.add_cascade(label='File', menu=file_menu)

menu_bar.add_command(label='Search')

tlabel = ttk.Label(root, text='Start keeping track of everything by...', font=Font(family="Arial", size=14), justify='right').pack()
tbutn1 = ttk.Button(root, text='Creating new diagram', bootstyle='primary outline', command=new_tree_view).pack(padx=4, pady=(6,4), anchor='w')
tbutn2 = ttk.Button(root, text='Opening a diagram', command=reconstruct_tree, bootstyle='info outline').pack(padx=4, pady=(0,4), anchor='w')

root.mainloop()