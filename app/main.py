import json
import math

from app.modules.customer import Customer
from app.modules.shop import Shop


def calculate_distance_between_points(
    point1: list[int],
    point2: list[int],
) -> float:
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def calculate_trip_cost(
    customer: Customer,
    shop: Shop,
    fuel_price: float,
) -> float:
    distance_to_shop = calculate_distance_between_points(
        shop["location"],
        customer["location"],
    )

    fuel_cost = (
        distance_to_shop * customer["car"]["fuel_consumption"]
        / 100 * fuel_price * 2
    )

    product_cost = sum(
        shop["products"][product] * customer["product_cart"][product]
        for product in customer["product_cart"].keys()
    )
    return round(fuel_cost + product_cost, 2)


def shop_in_store(customer: Customer, shop: Shop) -> None:
    print("Date: 04/01/2021 12:33:41")
    print(f'Thanks, {customer["name"]}, for your purchase!')
    print("You have bought:")
    total_cost = 0
    for product, quantity in customer["product_cart"].items():
        cost = quantity * shop["products"][product]
        total_cost += cost
        cost = int(cost) if cost % 1 == 0 else cost
        print(f"{quantity} {product}s for {(cost)} dollars")

    print(f"Total cost is {total_cost} dollars")
    print("See you again!\n")


def shop_trip() -> None:
    with open("app/config.json", "r") as file:
        config = json.load(file)

    fuel_price: float = config["FUEL_PRICE"]
    customers: list[Customer] = config["customers"]
    shops: list[Shop] = config["shops"]

    for customer in customers:
        print(f'{customer["name"]} has {customer["money"]} dollars')

        shopping_price: dict[str, float] = {}

        for shop in shops:
            shopping_price[shop["name"]] = calculate_trip_cost(
                customer,
                shop,
                fuel_price
            )

            print(
                f"{customer["name"]}'s trip to the {shop["name"]} "
                f'costs {shopping_price[shop["name"]]}'
            )

        cheapest_shop_name = min(shopping_price, key=shopping_price.get)

        if shopping_price[cheapest_shop_name] > customer["money"]:
            print(
                f'{customer["name"]} doesn\'t have'
                f" enough money to make a purchase in any shop"
            )
            continue

        print(f'{customer["name"]} rides to {cheapest_shop_name}\n')

        cheapest_shop = next(
            shop for shop in shops
            if shop["name"] == cheapest_shop_name
        )

        shop_in_store(customer, cheapest_shop)

        print(f'{customer["name"]} rides home')
        customer["money"] -= shopping_price[cheapest_shop_name]

        print(f'{customer["name"]} now has {customer["money"]} dollars\n')
