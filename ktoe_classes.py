class Location:
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list[Place] = []
        self.child_names = []
    def add_child(self, child: Place):
        if child.name not in self.child_names:
            child.set_location(self)
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

class Place:
    def __init__(self, name: str):
        self.name = name
        self.location = None
        self.children = []
        self.child_names = []
    def add_child(self, child: Place | Object):
            if child.name not in self.child_names:
                child.set_location(self)
                self.children.append(child)
                self.child_names.append(child.name)
                return True
            else:
                return False
    def set_location(self, location: Location | Place):
        self.location = location
    def child(self, name: str) -> Place | Object | Error:
        if name in self.child_names:
            return self.children[self.child_names.index(name)]
        else:
            return Error(name)

class Error(Place):
    def __init__(self, name: str):
        self.name = name

class Object:
    def __init__(self, name: str) -> None:
        self.name = name
    def set_location(self, location: Location | Place):
        self.location = location