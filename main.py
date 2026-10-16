import ttkbootstrap as ttk
from ktoe_classes import *
root = ttk.App(title='KeepTrackOfEverything')
root.theme_use('bootstrap-dark')

the_frame = ttk.Frame(root)
tree = Location("Room", the_frame)

def tree_view():
    global root, the_frame, tree
    ttk.Button(root, text=tree.name, command=tree.click, bootstyle='primary').pack()
    the_frame.pack()

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

tree_view()

root.mainloop()