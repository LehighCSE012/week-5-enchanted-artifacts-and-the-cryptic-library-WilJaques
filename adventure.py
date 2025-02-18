# Your code goes here
""" adventure game """
from hmac import new
import random

def display_player_status(player_stats):
    """ Display Player Status """
    #getting the health value from the dictionary
    print("Your current health:", player_stats.get("health"))

def handle_path_choice(player_stats):
    """ Handle Path Choice """
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_stats["health"] += 10
        player_stats["health"] = min(player_stats["health"], 100)
    else:
        print("You fall into a pit and lose 15 health points.")
        player_stats["health"] -= 15
        if player_stats["health"] < 0:
            player_stats["health"] = 0
            print("You are barely alive!")
    return player_stats["health"]

def player_attack(monster_health, player_stats):
    """ Player Attack """
    print("You strike the monster for 15 damage!")
    updated_monster_health = monster_health - player_stats["attack"]
    return updated_monster_health

def monster_attack(player_stats):
    """" Monster Attack """
    crit = random.randint(0,1)
    if crit <= .5:
        print("The monster lands a critical hit for 20 damage!")
        player_stats["health"] -= 20
    else:
        print("The monster hits you for 10 damage!")
        player_stats["health"] -= 10
    return player_stats["health"]

def combat_encounter(player_stats, monster_health, has_treasure):
    """" Combat Encounter """
    while player_stats["health"] > 0 and monster_health > 0:
        monster_health = player_attack(monster_health, player_stats)
        display_player_status(player_stats)
        if monster_health > 0:
            player_stats["health"] = monster_attack(player_stats)
    if player_stats["health"] <= 0:
        print("Game Over!")
        return False
    if monster_health <= 0:
        print("You defeated the monster!")
    return has_treasure # boolean

def check_for_treasure(has_treasure):
    """" Check for Treasure """
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def acquire_item(inventory, item):
    """ Acquire Item """
    inventory.append(item)
    print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """ Display Inventory """
    if len(inventory) == 0:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for index, item in enumerate(inventory, start=1):  # Start counting from 1
            print(f"{index}. {item}")

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """ Enter Dungeon """
    for rooms in dungeon_rooms:
        # the * allows for there to be No challege outcome
        room_description, item, challenge_type, *challenge_outcome = rooms
        print(room_description)
        try:
            rooms[0] = "trying to change the tuple"
        except TypeError as e:
            print("Error: Cannot modify room tuples - they are immutable.")
        if room_description == "bypass":
            print("You bypass the challenge.")
            player_stats["health"] += challenge_outcome[2]
            continue
        if item:
            print(f"You found a {item} in the room.")
            inventory = acquire_item(inventory, item)
        if challenge_type == "puzzle":
            print("You encounter a puzzle!")
            skip = input("Do you want to skip or solve the puzzle?")
            if skip == "skip":
                print("You skipped the puzzle.")
            else:
                if random.choice([True, False]):
                    print(challenge_outcome[0])
                    player_stats["health"] += challenge_outcome[2]
                else:
                    print(challenge_outcome[1])
                    player_stats["health"] += challenge_outcome[2]

        elif challenge_type == "trap":
            print("You see a potential trap!")
            disarm = input("Do you want to disarm or bypass the trap?")
            if  disarm == "disarm":
                if random.choice([True, False]):
                    print(challenge_outcome[0])
                    player_stats["health"] += challenge_outcome[2] * -1
                else:
                    print(challenge_outcome[1])
                    player_stats["health"] += challenge_outcome[2]
        elif challenge_type == "none":
            print("There doesn't seem to be a challenge in this room. You move on.")
        elif challenge_type == "library":
            print("You enter the Cryptic Library.")
            new_clue = ["The treasure is hidden where the dragon sleeps.",
                        "The key lies with the gnome.",
                        "Beware the shadows.",
                        "The amulet unlocks the final door.",
                        "This is not a clue."]
            rand_clues = random.sample(new_clue, 2)
            clues.update(find_clue(clues, rand_clues[0]))
            clues.update(find_clue(clues, rand_clues[1]))
            if "staff_of_wisdom" in artifacts:
                print("The Staff of Wisdom hums in your hand")
                print("You feel you could now bypass a puzzle")
                room_name = input("Enter the room name:")
                for i, room in enumerate(dungeon_rooms):
                    if room[0] == room_name:
                        outcome = dungeon_rooms[i][3][2]
                        dungeon_rooms.remove(room)  # Replace tuple
                        dungeon_rooms.append("Bypass", None, "none", (None, None, outcome))
                        break
        if player_stats["health"] <= 0:
            print("You are barely alive!")

        display_inventory(inventory)
    return player_stats, inventory, clues

def discover_artifact(player_stats, artifacts, artifact_name):
    """ Discover Artifact """
    if artifact_name in artifacts:
        print(artifacts[artifact_name]["description"])
        if artifacts[artifact_name]["effect"] == "increases health":
            #I am updating the health value in the dictionary
            player_stats.update({"health": artifacts[artifact_name]["power"]
                                 + player_stats["health"]})
            print("Your health has increased!")
            del artifacts[artifact_name]
        elif artifacts[artifact_name]["effect"] == "enhances attack":
            #I am updating the power value in the dictionary
            player_stats.update({"attack": artifacts[artifact_name]["power"]
                                 + player_stats["attack"]})
            print("Your attack has increased!")
            del artifacts[artifact_name]
        else:
            print("You found nothing of interest.")
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """ Find Clue """
    if new_clue not in clues:
        #adding the new clue to the set
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues


def main():
    """ Main Function """
    player_health = 100
    monster_health = 70 # Example hardcoded value
    inventory = []
    clues = set()

    artifacts = {
        "amulet_of_vitality": {
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "A powerful ring that boosts your attack damage.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "A staff imbued with ancient wisdom.",
            "power": 5,
            "effect": "solves puzzles"
    }
    }
    player_stats = {"health": player_health, "attack": 5}

    dungeon_rooms = [
    ("A dusty old library", "key", "puzzle",
     ("You solved the puzzle!", "The puzzle remains unsolved.", -5)),
    ("A narrow passage with a creaky floor", None, "trap",
      ("You skillfully avoid the trap!", "You triggered a trap!", -10)),
    ("A grand hall with a shimmering pool", "healing potion", "none", None)
    ]
    new_room = [("A small room with a locked chest", "treasure", "puzzle",
                    ("You cracked the code!", "The chest remains stubbornly locked.", -5))]
    # I am using this to change the last element to this new tuple
    dungeon_rooms.extend(new_room)
    # I am then using this to remove last element and test the pop function
    dungeon_rooms.pop()

    dungeon_rooms.append(("A vast library filled with ancient, cryptic texts.",
                           None, "library", None))

    player_stats["health"] = handle_path_choice(player_stats)

    treasure_obtained_in_combat = combat_encounter(player_stats, monster_health,
                                 random.choice([True, False]) # Randomly assign treasure
)
    if random.choice([True, False]):
        discover_artifact(player_stats, artifacts, random.choice(list(artifacts.keys())))
        #Getting the values of player status because the values are the health and attack values
        print("Players Health and Attack:", player_stats.values())
    check_for_treasure(treasure_obtained_in_combat) # Or has_treasure, depending on logic

    player_stats, inventory, clues = enter_dungeon(player_stats, inventory,
                                             dungeon_rooms, clues, artifacts)
    print(player_stats["health"])

if __name__ == "__main__":
    main()
