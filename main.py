import ttkbootstrap as ttk
from ktoe_classes import *
root = ttk.App(title='KeepTrackOfEverything')
root.theme_use('bootstrap-dark')

the_frame = ttk.Frame(root)
tree = Location("Room", the_frame)

def tree_view():
    global root, the_frame
    ttk.Button(root, text=tree.name, command=tree.click, bootstyle='primary').pack()
    the_frame.pack()


tree_view()

root.mainloop()