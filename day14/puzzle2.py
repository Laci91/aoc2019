import copy
import math
from itertools import chain

import parse

import file_utils


class RecipeItem:
    def __init__(self, name, count):
        self.name = name
        self.count = count

    def __repr__(self):
        return "%d %s" % (self.count, self.name)


class Recipe:
    def __init__(self, chemical, count, items):
        self.chemical = chemical
        self.count = count
        self.items = items

    def __repr__(self):
        return "%s => %s" % (self.chemical, ", ".join([i.__repr__() for i in self.items]))


def get_multiplier_for_ingredient(item, recipes):
    recipe = [recipes[r] for r in recipes if r.name == item.chemical.name][0]
    result_count = recipe.result.count
    return math.ceil(item.count / result_count)


def find_active_chemical(recipes):
    for chemical in recipes:
        if chemical not in map(lambda i: i.name, chain.from_iterable([recipes[i].items for i in recipes])):
            return recipes[chemical]


def calculate_ore_count(recipes, fuel):
    recipes["FUEL"].count = fuel
    ore = 0
    while len(recipes) > 0:
        next_recipe = find_active_chemical(recipes)
        recipes.pop(next_recipe.chemical.name)
        multiplier = math.ceil(next_recipe.count / next_recipe.chemical.count)
        print("Next to be removed: %s, with modifier %d" % (next_recipe.chemical.name, multiplier))

        for i in next_recipe.items:
            if i.name not in recipes:
                ore += multiplier * i.count
                print("Ore count increased by %d because of count %d" % (multiplier * i.count, next_recipe.count))
            else:
                r = recipes[i.name]
                r.count += multiplier * i.count
                print("Increased count of %s with %d to %d" % (i.name, multiplier * i.count, r.count))

    return ore


if __name__ == "__main__":
    lines = file_utils.read_lines("input14.txt")
    recipes = {}
    parser = parse.Parser("{} => {}")
    for line in lines:
        recipe_line = parser.parse(line)
        result_full = recipe_line[1].split(" ")

        ingredients = []
        for ingredient in recipe_line[0].split(", "):
            res_full = ingredient.split(" ")
            ingredients.append(RecipeItem(res_full[1], int(res_full[0])))

        main_item = RecipeItem(result_full[1], int(result_full[0]))
        recipes[main_item.name] = Recipe(main_item, 0 if main_item.name != "FUEL" else 1, ingredients)

    ore_count = 1
    next_ore_count = 1
    fuel_count = 1
    ore_limit = 1000000000000
    while not ore_count < ore_limit < next_ore_count:
        if ore_count != next_ore_count:
            fuel_count = math.floor(fuel_count * ore_limit / ore_count)
        ore_count = calculate_ore_count(copy.deepcopy(recipes), fuel_count)
        next_ore_count = calculate_ore_count(copy.deepcopy(recipes), fuel_count + 1)
        print("New fuel count: %s produces ore count %d, next ore count is %d (%d)" % (fuel_count, ore_count, next_ore_count, fuel_count + 1))

    print(math.floor(fuel_count))




