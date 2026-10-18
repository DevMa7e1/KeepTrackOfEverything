import ttkbootstrap as ttk
from functools import partial
from tkinter import Variable
from time import process_time_ns
from ttkbootstrap.dialogs import Messagebox

class Location:
    def __init__(self, name: str, root: ttk.Frame) -> None:
        self.name = name
        self.children: list[Place] = []
        self.child_names = []
        self.root = root
        self.frames = []
        self.id = process_time_ns()
    def add_child(self, child: Place):
        if child.name not in self.child_names:
            child.set_location(self, self.frames[-1], self.root)
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
        if name.get() not in self.child_names:
            self.frames.append(ttk.Frame(self.root, relief='solid', borderwidth=1).grid(row=2, column=len(self.frames), padx=4, pady=(0, 4), sticky='n'))
            np = Place(name.get())
            ttk.Button(self.root, text=name.get(), command = np.click, bootstyle='success').grid(row=1, column=len(self.frames)-1, padx=4, pady=(4, 0))
            self.add_child(np)
            window.destroy()
        else:
            Messagebox.ok('Cannot add an Object/Place with the same name as another Object/Place withing the same Location.', 'User error', parent=window)
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
        self.children: list[Place|Object] = []
        self.child_names = []
        self.frames = []
        self.root = None
        self.id = process_time_ns()
        self.button = None
    def add_child(self, child: Place | Object):
            if child.name not in self.child_names:
                if type(child) == Object:
                    child.set_location(self, None)
                else:
                    child.set_location(self, self.frames[-1], self.root) #type: ignore
                self.children.append(child)
                self.child_names.append(child.name)
                return True
            else:
                return False
    def set_location(self, location: Location | Place, root: ttk.Frame, actualroot: ttk.Frame):
        self.location = location
        self.root = root
        self.button = actualroot.children[list(actualroot.children.keys())[-1]]
    def child(self, name: str) -> Place | Object | Error:
        if name in self.child_names:
            return self.children[self.child_names.index(name)]
        else:
            return Error(name)
    def __after_add_click(self, name: ttk.Entry, selected: Variable, window: ttk.Toplevel):
        if name.get() not in self.child_names:
            if selected.get() == 'Place':
                self.frames.append(ttk.Frame(self.root, relief='solid', borderwidth=1).grid(row=2+(len(self.children)//5*2), column=len(self.children) % 5, padx=4, pady=(0, 4), sticky='n'))
                np = Place(name.get())
                ttk.Button(self.root, text=name.get(), command = np.click, bootstyle='warning').grid(row=1+(len(self.children)//5*2), column=len(self.children) % 5, padx=4, pady=(4, 0))
                self.add_child(np)
            else:
                ttk.Button(self.root, text=name.get()).grid(row=1+(len(self.children)//5*2), column=len(self.children) % 5, padx=4, pady=4)
                self.add_child(Object(name.get()))
            window.destroy()
        else:
            Messagebox.ok('Cannot add an Object/Place with the same name as another Object/Place withing the same Place.', 'User error', parent=window)
    def __add_click(self, none = None):
        window = ttk.Toplevel(title='Add a new Place or Object')
        window.resizable(width=False, height=False)
        ttk.Label(window, text='Name:', justify='left').pack(fill='x', expand=True, pady=(4, 0))
        name = ttk.Entry(window).pack(padx=(0, 4), pady=4)
        selected = Variable()
        ttk.OptionMenu(window, selected, 'Object', 'Place', 'Object').pack(padx=4, pady=4)
        ttk.Button(window, text='Add', command=partial(self.__after_add_click, name, selected, window), bootstyle='primary').pack(padx=4, pady=4)
    def __after_rename_click(self, entry: ttk.Entry, window):
        newname = entry.get()
        self.name = newname
        self.button.config(text=newname) #type: ignore
        window.destroy()
    def __rename_click(self, none = None):
        window = ttk.Toplevel(title=f'Rename {self.name}')
        window.resizable(width=False, height=False)
        ttk.Label(window, text='New name:', justify='left').pack(fill='x', expand=True, pady=(4, 0))
        name = ttk.Entry(window).pack(padx=(0, 4), pady=4)
        ttk.Button(window, text='Rename', command=partial(self.__after_rename_click, name, window), bootstyle='primary').pack(padx=4, pady=4)
    def click(self):
        window = ttk.Toplevel(title=self.name)
        window.resizable(width=False, height=False)
        ttk.Label(window, text='What would you like to do?').pack(anchor='e', pady=4)
        ttk.Button(window, text='Add a new Object or Place', bootstyle='info outline', command=lambda: self.__add_click(window.destroy())).pack(anchor='w', padx=4, pady=4)
        ttk.Button(window, text='Rename this Place', bootstyle='danger outline', command=lambda: self.__rename_click(window.destroy())).pack(anchor='w', padx=4, pady=(0,4))

class Error(Place):
    def __init__(self, name: str):
        self.name = name
        self.id = 0

class Object:
    def __init__(self, name: str) -> None:
        self.name = name
        self.id = process_time_ns()
        self.button = None
    def set_location(self, location: Location | Place, root):
        self.location = location

class BasicTree:
    def __init__(self, owner: Location|Place):
        self._d = {}
        self._owner = owner
    def __getitem__(self, key) -> BasicTree:
        return self._d[key]
    def __setitem__(self, key: Object|Place, value: BasicTree):
        self._d[key] = value
    def __str__(self) -> str:
        return str(self._d)
    def __contains__(self, item):
        return item in self._d
    def children(self):
        return list(self._d.keys())
    def owner(self):
        return self._owner