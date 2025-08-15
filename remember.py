def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

print(get_full_name("john", "doe"))


def get_name_with_age(name: str, age: str):
    name_with_age = name + " is this old: " + age
    return name_with_age
print(get_name_with_age("Daniel", "23"))

def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_e

def procces_items(items: list[str]):
    for item in items:
        print(item)
        
def procces_items(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_s

def process_items(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)
process_items({"daniel":10})