import ttkbootstrap as ttk
from functools import partial
from tkinter import Variable

class Location:
    def __init__(self, name: str, root: ttk.Frame) -> None:
        self.name = name
        self.children: list[Place] = []
        self.child_names = []
        self.root = root
        self.frames = []
    def add_child(self, child: Place):
        if child.name not in self.child_names:
            child.set_location(self, self.frames[-1])
            self.children.append(child)
            self.child_names.append(child.name)
            return True
        else:
            return False
    def child(self, name: str) -> Place | Error:
        if name in self.child_names:
            return self.children[self.child_names.index(name)]
        else:
            return Error(name)
    def __after_click(self, name: ttk.Entry, window: ttk.Toplevel):
        self.frames.append(ttk.Frame(self.root, relief='solid', borderwidth=1).grid(row=2, column=len(self.frames), padx=4, pady=(0, 4), sticky='n'))
        np = Place(name.get())
        ttk.Button(self.root, text=name.get(), command = np.click, bootstyle='success').grid(row=1, column=len(self.frames)-1, padx=4, pady=(4, 0))
        self.add_child(np)
        window.destroy()
    def click(self):
        window = ttk.Toplevel(title='Add a new Place')
        window.resizable(width=False, height=False)
        ttk.Label(window, text='Name:', justify='left').pack(fill='x', expand=True, padx=(0, 4))
        name = ttk.Entry(window).pack(padx=(0, 4), pady=4)
        ttk.Button(window, text='Add', command=partial(self.__after_click, name, window), bootstyle='primary').pack(padx=4, pady=4)

class Place:
    def __init__(self, name: str):
        self.name = name
        self.location = None
        self.children = []
        self.child_names = []
        self.frames = []
        self.root = None
    def add_child(self, child: Place | Object):
            if child.name not in self.child_names:
                if type(child) == Object:
                    child.set_location(self, None)
                else:
                    child.set_location(self, self.frames[-1])
                self.children.append(child)
                self.child_names.append(child.name)
                return True
            else:
                return False
    def set_location(self, location: Location | Place, root):
        self.location = location
        self.root = root
    def child(self, name: str) -> Place | Object | Error:
        if name in self.child_names:
            return self.children[self.child_names.index(name)]
        else:
            return Error(name)
    def __after_click(self, name: ttk.Entry, selected: Variable, window: ttk.Toplevel):
        if selected.get() == 'Place':
            self.frames.append(ttk.Frame(self.root, relief='solid', borderwidth=1).grid(row=2, column=len(self.children), padx=4, pady=(0, 4), sticky='n'))
            np = Place(name.get())
            ttk.Button(self.root, text=name.get(), command = np.click, bootstyle='warning').grid(row=1, column=len(self.children), padx=4, pady=(4, 0))
            self.add_child(np)
        else:
            ttk.Button(self.root, text=name.get()).grid(row=1, column=len(self.children), padx=4, pady=4)
            self.add_child(Object(name.get()))
        window.destroy()
    def click(self):
        window = ttk.Toplevel(title='Add a new Place or Object')
        window.resizable(width=False, height=False)
        ttk.Label(window, text='Name:', justify='left').pack(fill='x', expand=True, pady=(4, 0))
        name = ttk.Entry(window).pack(padx=(0, 4), pady=4)
        selected = Variable()
        ttk.OptionMenu(window, selected, 'Object', 'Place', 'Object').pack(padx=4, pady=4)
        ttk.Button(window, text='Add', command=partial(self.__after_click, name, selected, window), bootstyle='primary').pack(padx=4, pady=4)

class Error(Place):
    def __init__(self, name: str):
        self.name = name

class Object:
    def __init__(self, name: str) -> None:
        self.name = name
    def set_location(self, location: Location | Place, root):
        self.location = location