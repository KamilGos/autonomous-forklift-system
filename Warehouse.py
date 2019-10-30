

class Warehouse():
    def __init__(self):
        self.stack = []

    def push(self, id):
        self.stack.append(id)

    def pop(self):
        if len(self.stack)<1:
            return None
        return self.stack.pop()

    def size(self):
        return len(self.stack)

    def Show_Stack(self):
        print("--TOP--")
        for elem in self.stack[::-1]: print(elem)
        print("-FLOOR-")





if __name__=="__main__":
    Warehouse = Warehouse()
    Warehouse.push(1)
    Warehouse.push(2)
    Warehouse.push(3)
    Warehouse.Show_Stack()
    print("I poped: ", Warehouse.pop())
    Warehouse.Show_Stack()
    print("Size: ", Warehouse.size())
