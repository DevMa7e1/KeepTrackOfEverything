import ttkbootstrap as ttk
from ktoe_classes import *
root = ttk.App(title='KeepTrackOfEverything')
root.theme_use('bootstrap-dark')

tree = Location("Room")
tree.add_child(Place("Box"))
tree.add_child(Place("Box 2"))
tree.child("Box").add_child(Object("Ornamental box 1"))
tree.child("Box").add_child(Object("Ornamental box 2"))
tree.child("Box 2").add_child(Object("Ornamental box 3"))
tree.child("Box 2").add_child(Object("Ornamental box 4"))


def tree_view():
    global root
    ttk.Label(root, text=tree.name).grid(row=0, column=0)

    the_frame = ttk.Frame(root)
    the_frame.grid(row=1, column=0)
    col = 0
    frames = []
    for name in tree.child_names:
        frames.append(ttk.Frame(the_frame, relief='solid', borderwidth=1).grid(row=2, column=col, padx=4, pady=4))
        ttk.Label(the_frame, text=name, justify='center').grid(row=1, column=col)
        col += 1
    col = 0
    frame = 0
    frames2 = []
    for placename in tree.child_names:
        for name in tree.child(placename).child_names:
            frames2.append(ttk.Frame(frames[frame], relief='solid', borderwidth=1).grid(row=2, column=col, padx=4, pady=4))
            ttk.Label(frames[frame], text=name).grid(row=1, column=col)
            col += 1
        col = 0
        frame += 1

tree_view()

root.mainloop()