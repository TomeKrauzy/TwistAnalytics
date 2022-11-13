class CostsUnitContainer:
    def __init__(self, name, **subcategories):
        self.name = name
        # Updates dictionary that stores class properties
        self.__dict__.update(subcategories)

