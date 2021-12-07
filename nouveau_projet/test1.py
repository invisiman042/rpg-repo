class Entity:
	def __init__(self, name, health, strength, defense):
		self.name = name
		self.health = health
		self.strength = strength
		self.defense = defense

	def get_info(self):
		return f'Name : {self.name} Health : {self.health} Strength : {self.strength} Defense : {self.defense}'

	def attacks(self, enemy):
		attack_force = self.strength - enemy.defense
		print(self.name, 'attacks', enemy.name)
		enemy.health -= attack_force
		print(enemy.name, 'takes', attack_force, 'damage', f'({self.strength} - {enemy.defense})')


adventurer1 = Entity('Hector', 10, 2, 3)
monster1 = Entity('Troll', 4, 2, 1)

print(adventurer1.get_info())
print(monster1.get_info())

adventurer1.attacks(monster1)

print(adventurer1.get_info())
print(monster1.get_info())
# import dungeon_crawler

# dungeon_crawler.main_prog()