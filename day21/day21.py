from dataclasses import dataclass
from pprint import pprint
from typing import Tuple, Set, Dict


def test_silver_example():
    foods = parse("example.txt")
    assert all_allergens(foods) == {'soy', 'dairy', 'fish'}
    assert all_ingredients(foods) == {'trh', 'fvjkl', 'sbzzf', 'nhms', 'mxmxvkd', 'sqjhc', 'kfcds'}
    assert allergen_occurence(foods)["dairy"]["mxmxvkd"] == 2
    assert most_common_ingredient_for_allergen(foods) == {
        'dairy': {'mxmxvkd'},
        'fish': {'mxmxvkd', 'sqjhc'},
        'soy': {'fvjkl', 'sqjhc'},
    }
    assert all_ingredients_with_allergen(foods) == {'mxmxvkd', 'sqjhc', 'fvjkl'}
    assert 5 == occurence_ingredients_without_allergens(foods)


def test_silver():
    foods = parse("input.txt")
    pprint(most_common_ingredient_for_allergen(foods))
    assert 2282 == occurence_ingredients_without_allergens(foods)


def test_gold_example():
    foods = parse("example.txt")
    assert cannonical_dangerous_ingredient_list(foods) == "mxmxvkd,sqjhc,fvjkl"


def test_gold():
    foods = parse("input.txt")
    assert cannonical_dangerous_ingredient_list(foods) == "vrzkz,zjsh,hphcb,mbdksj,vzzxl,ctmzsr,rkzqs,zmhnj"


def cannonical_dangerous_ingredient_list(foods) -> str:
    dangerous_ingredients_dict = create_dangerous_ingredients_dict(foods)
    return ",".join(
        map(
            lambda item: item[0],
            sorted(
                dangerous_ingredients_dict.items(),
                key=lambda item: item[1]
            )
        )
    )


def create_dangerous_ingredients_dict(foods):
    possible_ingredients_per_allergen: Dict[str, Set[str]] = most_common_ingredient_for_allergen(foods)
    dangerous_ingredients_dict = {}
    while len(dangerous_ingredients_dict) < len(all_allergens(foods)):
        dangerous_ingredients_dict = {
            **dangerous_ingredients_dict,
            **{
                tuple(ingredients)[0]: allergen
                for allergen, ingredients in possible_ingredients_per_allergen.items()
                if len(ingredients) == 1
            }
        }
        possible_ingredients_per_allergen = {
            allergen: ingredients.difference(set(dangerous_ingredients_dict.keys()))
            for allergen, ingredients in possible_ingredients_per_allergen.items()
        }
    return dangerous_ingredients_dict


def occurence_ingredients_without_allergens(foods):
    return sum(
        occurence
        for ingredient, occurence in ingredient_occurences(foods).items()
        if ingredient not in all_ingredients_with_allergen(foods)
    )


def ingredient_occurences(foods):
    return {
        ingredient: sum(
            1
            for food in foods
            if ingredient in food.ingredients
        )
        for ingredient in (all_ingredients(foods))
    }


def all_ingredients_with_allergen(foods):
    return set.union(*most_common_ingredient_for_allergen(foods).values())


def most_common_ingredient_for_allergen(foods):
    return {
        allergen: {
            ingredient
            for ingredient, occurence in occurences.items()
            if occurence == max(occurences.values())
        }
        for allergen, occurences in allergen_occurence(foods).items()
    }


def allergen_occurence(foods):
    return {
        allergen: {
            ingredient: sum(
                1
                for food in foods
                if food.contains(ingredient, allergen)
            )
            for ingredient in all_ingredients(foods)
        }
        for allergen in (all_allergens(foods))
    }


@dataclass(frozen=True)
class Food:
    ingredients: Set[str]
    allergens: Set[str]

    @staticmethod
    def parse(line: str) -> "Food":
        ingredients, allergens = line[:-1].split(" (contains ")
        return Food(
            set(ingredients.split(" ")),
            set(allergens.split(", ")),
        )

    def contains(self, ingredient: str, allergen: str) -> bool:
        return ingredient in self.ingredients and allergen in self.allergens


def all_allergens(foods: Tuple[Food]) -> Set[str]:
    return {
        allergen
        for food in foods
        for allergen in food.allergens
    }


def all_ingredients(foods: Tuple[Food]) -> Set[str]:
    return {
        ingredient
        for food in foods
        for ingredient in food.ingredients
    }


def parse(file_name: str) -> Tuple[Food]:
    with open(file_name) as file:
        return tuple(
            Food.parse(line)
            for line in file.read().split("\n")
        )
