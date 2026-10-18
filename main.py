import ttkbootstrap as ttk
from ttkbootstrap.dialogs import filedialog, Messagebox
from ktoe_classes import *
import dill
from tkinter.font import Font

root = ttk.App(title='KeepTrackOfEverything')
root.theme_use('bootstrap-dark')

def asksave(tree, window):
    result = Messagebox.yesnocancel('Would you like to save your diagram?', 'KeepTrackOfEverything', parent=window)
    if result == 'Yes':
        deconstruct_tree(tree, window)
    elif result == 'No':
        window.destroy()

def tree_view(name: str | ttk.Entry, window = None):
    if type(name) == ttk.Entry:
        name = name.get()
    toplevel = ttk.Toplevel(title=name) #type: ignore
    menu_bar = ttk.Menu(toplevel)
    toplevel.config(menu=menu_bar)
    toplevel.grid_rowconfigure(0, weight=1)
    toplevel.grid_rowconfigure(2, weight=0)
    toplevel.grid_columnconfigure(0, weight=1)
    toplevel.grid_columnconfigure(2, weight=0)

    file_menu = ttk.Menu(menu_bar)
    file_menu.add_command(label='Load diagram', command=reconstruct_tree)
    menu_bar.add_cascade(label='File', menu=file_menu)
    canvas = ttk.Canvas(toplevel, width=750, height=500)

    the_frame = ttk.Frame(toplevel)
    scrollbar1 = ttk.Scrollbar(toplevel, orient="vertical", command=canvas.yview)
    scrollbar1.grid(row = 0, column = 1, sticky='ns')
    scrollbar2 = ttk.Scrollbar(toplevel, orient="horizontal", command=canvas.xview)
    scrollbar2.grid(row = 2, column = 0, sticky='ew')
    canvas.configure(yscrollcommand=scrollbar1.set, xscrollcommand=scrollbar2.set)
    
    canvas.create_window((0, 0), window=the_frame, anchor="n")
    the_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    anotherframe = ttk.Frame(the_frame)
    tree = Location(name, anotherframe) #type: ignore
    file_menu.add_command(label='Save diagram and close', command=partial(deconstruct_tree, tree, toplevel))
    file_menu.add_command(label='Quit', command=quit)
    menu_bar.add_command(label='Search', command=partial(search_window, tree))
    ttk.Button(the_frame, text=tree.name, command=tree.click, bootstyle='primary').grid(row=0, column=0)
    anotherframe.grid(row=1, column=0)
    canvas.grid(row=0, column=0, sticky='news')
    if window != None:
        window.destroy()
    toplevel.protocol('WM_DELETE_WINDOW', partial(asksave, tree, toplevel))
    return the_frame, tree

def search_window(tree):
    window = ttk.Toplevel(title='Search box')
    window.resizable(width=False, height=False)
    ttk.Label(window, text='Query:', justify='left').pack(fill='x', expand=True, padx=(0, 4))
    query = ttk.Entry(window).pack(padx=(0, 4), pady=4)
    ttk.Button(window, text='Search', command=partial(search_tree, query, tree, window), bootstyle='primary').pack(padx=4, pady=4)

def new_tree_view():
    window = ttk.Toplevel(title='New diagram')
    window.resizable(width=False, height=False)
    ttk.Label(window, text='Name:', justify='left').pack(fill='x', expand=True, padx=(0, 4))
    name = ttk.Entry(window).pack(padx=(0, 4), pady=4)
    ttk.Button(window, text='Add', command=partial(tree_view, name, window), bootstyle='primary').pack(padx=4, pady=4)

def search_tree(query, tree, window = None):
    if type(query) == ttk.Entry:
            query = query.get()
    if window != None:
        window.destroy()
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

def deconstruct_tree(tree, window):
    places: list[Place] = []
    places2: list[Place] = []
    for i in tree.children:
        if type(i) == Place:
            places2.append(i)
            i.frames = []
        i.root = None
        i.button.destroy() #type: ignore
        i.button = None
    
    while len(places2) != 0:
        places = places2
        places2 = []
        for place in places:
            for i in place.children:
                if type(i) == Place:
                    places2.append(i)
                    i.frames = []
                    i.button.destroy() #type: ignore
                    i.button = None
                i.root = None #type: ignore
    tree.root = None #type: ignore
    tree.frames = []
    if save_tree(dill.dumps(tree)):
        window.destroy()

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
        return True
    else:
        return False

def load_tree():
    fd = filedialog.FileDialog(root, title='Open a diagram', filetypes=[('KeepTrackOfEverything diagram', '.ktoe')])
    fd.show()
    if fd.result != None:
        f = open(fd.result, 'rb') #type: ignore
        dump = f.read()
        return dump

def reconstruct_tree():
    dump = load_tree()
    tree = dill.loads(dump)
    frameish, tree2 = tree_view(tree.name)
    the_frame = ttk.Frame(frameish)
    the_frame.grid(row=1, column=0)
    frames = {}
    places = []
    places2 = []
    for i in tree.children:
        if i not in frames.keys():
            frames[i] = [ttk.Frame(the_frame, relief='solid', borderwidth=1).grid(row=2, column=len(frames.keys()), padx=4, pady=(0, 4), sticky='n'), 0]
        i.button = ttk.Button(the_frame, text=i.name, bootstyle='success', command=i.click).grid(row=1, column=len(frames.keys())-1, padx=4, pady=(4, 0))
        i.root = frames[i][0]
        tree.frames.append(frames[i])
        tree.add_child(i)
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
                    i.button = ttk.Button(frames[place][0], text=i.name, bootstyle='warning', command=i.click).grid(row=1, column=frames[place][1], padx=4, pady=(4, 0))
                else:
                    ttk.Button(frames[place][0], text=i.name, bootstyle='secondary').grid(row=1, column=frames[place][1], padx=4, pady=(4, 4))
                frames[place][1] += 1
                place.add_child(i)
    tree2.name = tree.name; tree2.children = tree.children; tree2.child_names = tree.child_names; tree2.id = tree.id

menu_bar = ttk.Menu(root)
root.config(menu=menu_bar)

file_menu = ttk.Menu(menu_bar)
file_menu.add_command(label='Load diagram', command=reconstruct_tree)
file_menu.add_command(label='Quit', command=quit)
menu_bar.add_cascade(label='File', menu=file_menu)

menu_bar.add_command(label='Search')

tlabel = ttk.Label(root, text='Start keeping track of everything by...', font=Font(family="Arial", size=14), justify='right').pack()
tbutn1 = ttk.Button(root, text='Creating new diagram', bootstyle='primary outline', command=new_tree_view).pack(padx=4, pady=(6,4), anchor='w')
tbutn2 = ttk.Button(root, text='Opening a diagram', command=reconstruct_tree, bootstyle='info outline').pack(padx=4, pady=(0,4), anchor='w')

root.resizable(width=False, height=False)
root.mainloop()