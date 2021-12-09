from random import choice, randint

class Character:
	def __init__(self):
		''' initialize character with empty name and unit health
		'''
		self.name = ""
		self.max_health = 1
		self.health = self.max_health

	def do_damage(self, enemy):
		''' do damages to the enemy, return if the enemy is dead
		'''
		damage = randint(0, 2)
		enemy.health -= damage
<<<<<<< HEAD
		if enemy.health > 0:
			print(f'!! {self.name} gives {damage} damage(s) to {enemy.name} !!\n{enemy.name} has now {enemy.health}/{enemy.max_health}')
		else:
			print(f'{enemy.name} is ded')
=======
		
		if damage == 0:
			print(f'! {self.name} gives {damage} damage to {enemy.name} !')
		elif damage == 1:
			print(f'! {self.name} gives {damage} damage to {enemy.name} !')
		else:
			print(f'! {self.name} gives {damage} damage(s) to {enemy.name} !')

		if not enemy.health <= 0:
			print(f'{enemy.name} has now {enemy.health}/{enemy.max_health}')
			
>>>>>>> a4e55596770242bd7f7de4ce622b52d7ccd18d05
		return enemy.health <= 0

	def status(self):
		''' display character name and health
		'''
		print(f'{self.name}, {self.health}/{self.max_health}, healing : {self.healing_pot}')

class Enemy(Character):
	def __init__(self, player):
		''' initialize player enemy with random name and random health
		'''
		super().__init__()
		self.name, self.max_health = choice([('gobelin', 1), ('dog', 2), ('bat', 3), ('wolf', 4), ('eagle', 5)])
		self.health = self.max_health

class Player(Character):
	def __init__(self):
		''' initialize player with 10 health and normal state by default
		'''
		super().__init__()
		self.state = 'normal'
		self.max_health = 10
		self.health = self.max_health
		self.healing_pot = 2

	def help(self):
		''' returns all commands
		'''
		print('Command list :', list(commands.keys()))

	def quit(self):
		''' quit the adventure
		'''
		print(f'{self.name} has surrendered his adventure')
		self.health = 0

	def attack(self):
		if self.state != 'fight':
			print(f'{self.name} is alone')
		else:
			if self.do_damage(self.enemy):
				print('monster killed, adventurer up')
<<<<<<< HEAD
				self.state = 'normal'
				self.max_health += 1
			elif self.enemy.do_damage(self):
				print('adventurer got kill by enemy')

	def counter(self):
		pass
=======
				self.max_health += 1
				self.state = 'normal'
				self.help
			elif self.enemy.do_damage(self):
				print('adventurer got hit by enemy')
>>>>>>> a4e55596770242bd7f7de4ce622b52d7ccd18d05
	
	def explore(self):
		if self.state != 'normal':
			print(f'{self.name} is busy')
		else:
			self.state = 'fight'
			self.enemy = Enemy(self)
			print(f'{self.name} encounters {self.enemy.name, self.enemy.health}')

	def heal(self):
<<<<<<< HEAD
		''' randomly gain health
		'''
		if self.state != 'normal':
			print(f'{self.name} can not recover now')
		elif self.healing_pot > 0:
			healing = randint(0, self.max_health - self.health)
=======
		''' use healing potion
		'''
		if self.state != 'normal':
			print(f'{self.name} can not rest now')
		elif self.health <= 0:
			healing = randint(0, self.max_health - self.health -1)
>>>>>>> a4e55596770242bd7f7de4ce622b52d7ccd18d05
			print(f'{self.name} has gained {healing} health')
			self.health += healing
			self.healing_pot -= 1
		else:
			print(f'{self.name} has no more healing potion')

def test_main():
	player = Player()
	player.name = 'Hector'#input("Player name :")
	monster = Enemy(player)

	player.status()
	monster.status()
	time_to_kill = 1
	while not player.do_damage(monster):
		player.status()
		monster.status()
		time_to_kill += 1
	print(f'{monster.name, monster.max_health} is dead in {time_to_kill} shots')

commands = {
	'help': Player.help,
	'quit': Player.quit,
	'attack': Player.attack,
	'explore': Player.explore,
	'status': Player.status,
	'rest': Player.heal
}

def main():
	player = Player()
	player.name = 'Hector'#input("Player name :")
	while player.health > 0:
		request = input('> ')
		for command in commands.keys():
			if command == request:
				commands[request](player)

if __name__ == '__main__':
	# test_main()
	main()