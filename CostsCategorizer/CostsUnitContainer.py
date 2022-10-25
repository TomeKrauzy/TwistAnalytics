class CostsUnitContainer():

    def __init__(self, name, **subcategories):
        self.name = name
        # Updatuje dict, która reprezentuje property classy
        self.__dict__.update(subcategories)

