#main function for bicycle project

from bicycle_classes import bicycle, bike_shop, customer

if __name__ == '__main__':

    # create bicycles and add them to a list
    kona = bicycle('lava dome', 20, 300)
    specialized = bicycle('stump jumper', 15, 700)
    giant = bicycle('rock hopper', 23, 150)
    trek = bicycle('roadster', 12, 100)
    scott = bicycle('downhill', 25, 400)
    cannondale = bicycle('crusier', 10, 180)

    inventory_list = [kona, specialized, giant, trek, scott, cannondale]

    # create a bike shop with the newly created bikes in their inventory
    sprockets = bike_shop('sprockets', inventory_list, .2)

    # create three customers and add them to a list
    jeff = customer('jeff', 200)
    ryan = customer('ryan', 500)
    danny = customer('danny', 1000)

    customers = [jeff, ryan, danny]

    # print the available inventory for sale and their prices
    print("Welcome to Sprockets! The following bikes are available for purchase:")

    for bicycle in sprockets.inventory:
        print(bicycle.model, "-", "retail price:", sprockets.retail(bicycle))

    # print each customer and their budget
    for customer in customers:
        print(customer.name, "has a budget of: $", customer.fund)

    # figure out which bikes each customer can afford
    for customer in customers:
        for bicycle in sprockets.inventory:
            if customer.fund >= sprockets.retail(bicycle):
                customer.affordable_bikes.append(bicycle)
                
    for customer in customers:
        print(customer.name, "Can afford the following bikes:")
        for bicycle in customer.affordable_bikes:
            print(bicycle.model)

    # have each customer purchase a bike
    for customer in customers:
        sprockets.purchase(customer)
        print(customer.name, "purchased a", customer.bikes_owned[0].model, "and has $", customer.fund, "left in their bike fund")
        print("Sprockets made", sprockets.profit(customer.bikes_owned[0]), "profit on the sale.")
      
    # print sprockets remaining inventory  
    print("Sprockets has these bikes left in their inventory:")  
    for bicycle in sprockets.inventory:
        print(bicycle.model)
