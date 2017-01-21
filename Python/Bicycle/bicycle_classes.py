# create the bicycle class
class bicycle(object):
    
    def __init__(self, model, weight, cost):
        self.model = model
        self.weight = weight
        self.cost = cost
    
# create the bike shop class    
class bike_shop(object):

    def __init__(self, name, inventory, profit_margin):
        self.name = name
        self.inventory = inventory
        self.profit_margin = profit_margin

    def retail(self, bicycle):
            retail_p = (1 + self.profit_margin) * bicycle.cost
            return retail_p
    
    def profit(self, bicycle):
        profit = self.profit_margin * bicycle.cost
        return profit

    def purchase(self, customer):
        if customer.affordable_bikes:
            customer.bikes_owned.append(customer.affordable_bikes[0])
            customer.fund = customer.fund - self.retail(customer.affordable_bikes[0])
            self.inventory = [bike for bike in self.inventory if bike not in customer.bikes_owned]

# create the customer class        
class customer(object):

    def __init__(self, name, fund):
        self.name = name
        self.fund = fund
        self.bikes_owned = []
        self.affordable_bikes = []
