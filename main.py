from classes.game import bcolors, persons
from classes.magic import spell
from classes.inventory import Item
import random


# Create Black magic
fire = spell("Fire", 19, 620, "black")
thunder = spell("Thunder", 22, 650, "black")
hammer = spell("Hammer", 17, 600, "black")
knife = spell("Knife", 15, 580, "black")
sword = spell("Sword", 14, 560, "black")

# Create White magic
cure = spell("Cure", 24, 720, "white")
cura = spell("Cura", 38, 1600, "white")
curaga = spell("Curaga", 55, 6000, "white")


# crete some items
potion = Item("Potion", "potion", "Heals 50 HP", 200)
hipotion = Item("HiPotion", "potion", "Heals 100 HP", 700)
superpotion = Item("SuperPotion", "potion", "Heals 500 HP", 3000)
elixer = Item("Elexer", "elexer", "Fully restore HP/MP of one party member", 9999)
megaelexer = Item("MegaElexer", "elexer", "Fully restore party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 5000)


player_spell = [fire, thunder, hammer, knife, sword, cura, cure]
enemy_spell = [fire, knife, cure]

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": megaelexer, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Instantiate people
player1 = persons("zaigger :", 3500, 250, 318, 30, player_spell, player_items)
player2 = persons("vikash  :", 3800, 260, 300, 30, player_spell, player_items)
player3 = persons("ankit   :", 3700, 270, 288, 30, player_spell, player_items)
# enemy
enemy1 = persons("kancha", 2500, 120, 565, 320, enemy_spell, [])
enemy2 = persons("kaliya", 17500, 300, 525, 20, enemy_spell, [])
enemy3 = persons("mamba ", 2000, 110, 560, 350, enemy_spell, [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]


running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "An Enemy attacks!" + bcolors.ENDC + "this is not normal text")

while running:
    print("===================================")

    print("\n\n")
    print("NAME                   HP                                     MP")

    for player in players:
        player.get_status()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_status()

    for player in players:


        player.choose_action()
        choice = input("    Choose option: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("you attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " is died!")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n Not enough mp \n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " is died!")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left ...." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + "HP" + bcolors.ENDC)

            elif item.type == "elexer":

                if item.name == "MegaElexer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + "fully restore HP/MP " + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " Deals " + str(item.prop) + " point of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " is died!")
                    del enemies[enemy]

    # check if battel is over
    defeated_enemies = 0
    defeayed_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeayed_players += 1

    # check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win" + bcolors.ENDC)
        running = False

    # check if enemy won
    elif defeayed_players == 2:
        print(bcolors.FAIL + " you lose!" + bcolors.ENDC)

        running = False
    print("\n")
    # enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # choose enemy
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacked" + players[target].name.replace(" ", "") + " for", enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals" + enemy.name + " for " + str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "' s" + spell.name + " deals " + str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " is died!")
                    del players[player]
            print("Enemy choose", spell, " magic is", magic_dmg)



