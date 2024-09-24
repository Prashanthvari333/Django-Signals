class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
    
    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}


# Usage example
rectangle = Rectangle(5, 3)
for item in rectangle:
    print(item)