import random

def roll(num):
	cur_roll = [random.randint(1,6) for i in range(num)]
	return cur_roll

def most_frequent(dice, rolled_dice):
	counts = {}
	for i in dice:
		if i not in counts:
			counts[i] = 1
		else:
			counts[i] += 1
	for i in rolled_dice:
		if i not in counts:
			counts[i] = 1
		else:
			counts[i] += 1
	most_frequent_die = '-'
	max_count = 0
	for i in counts:
		if counts[i] > max_count:
			max_count = counts[i]
			most_frequent_die = i
	return [most_frequent_die, max_count]

def dice_sum(dice):
	dice_sum = 0
	for i in dice:
		dice_sum += i
	return dice_sum

def cpu_turn(scoreboard):
	dice = []
	num_of_rolls = 0
	while num_of_rolls < 3:
		num_of_rolls += 1
		rolled_dice = roll(5 - len(dice))
		print(str(dice) + str(rolled_dice))
		target_category = most_frequent(dice, rolled_dice)[0]
		if num_of_rolls < 3:
			for i in rolled_dice:
				if i == target_category:
					dice.append(i)
		else:
			for i in rolled_dice:
				dice.append(i)
		if len(dice) > 5:
			print('asdf')
	print('Final: ' + str(dice))
	worst_case_target = 0
	while scoreboard[str(target_category)] != '-':
		if worst_case_target > 5:
			if scoreboard['random'] == '-':
				worst_case_target = 'random'
			else:
				worst_case_target = 'fullhouse'
		else:
			worst_case_target += 1
		target_category = worst_case_target

# ATTEMPTS TO PICK A SPECIAL CATEGORY

	if check_fullhouse(dice) and scoreboard['fullhouse'] == '-' and dice_sum(dice) > 15:
		target_category = 'fullhouse'
	elif dice_sum(dice) > 17 and scoreboard['random'] == '-':
		target_category = 'random'
	if check_yahtzee(dice):
		scoreboard['yahtzee'] += 25
	print(target_category)
	return score(dice, scoreboard, str(target_category))

def turn(scoreboard):
	dice = []
	num_of_rolls = 1

#	THIS IS THE PLAYER ROLL LOOP

	while num_of_rolls < 3:
		rolled_dice = roll(5 - len(dice))
		print(f"Roll {num_of_rolls}:  {dice} {rolled_dice}")
		choice = '-'

#	PLAYER CHOOSES TO KEEP, REMOVE, OR REROLL DICE (INDICES START AT 1, NOT 0)
#	THIS IS THE PLAYER CHOICE LOOP

		while True:
			choice = input('What would you like to do? (k for keep, r for remove, ENTER for pass): ')
			if choice not in ['k', 'r', '']:
				print('ERROR: INVALID INPUT')

			elif choice == 'r':
				remove = input('Remove any dice? (indices separated by commas): ')
#	FOR LOOP BECAUSE OF FUCKING PASS BY REFERENCE
				temp_dice = [die for die in dice]
				for char in remove:
					if char != ',':
						dice.remove(temp_dice[int(char) - 1])
						rolled_dice.append(temp_dice[int(char) - 1])
				print(f"{dice} {rolled_dice}")

			elif choice == 'k':
				keep = input('Keep any dice? (indices separated by commas): ')
#	FOR LOOP BECAUSE OF FUCKING PASS BY REFERENCE
				temp_dice = [die for die in rolled_dice]
				for char in keep:
					if char != ',':
						dice.append(rolled_dice[int(char) - 1])
						temp_dice.remove(rolled_dice[int(char) - 1])
				rolled_dice = temp_dice
				print(f"{dice} {rolled_dice}")				
			elif choice == '':
				num_of_rolls += 1
				break

		if len(dice) == 5:
			break

	if len(dice) < 5:
		final_roll = roll(5 - len(dice))
		for i in final_roll:
			dice.append(i)
	print('Final Roll: ' + str(dice))
	return score(dice, scoreboard)

def check_yahtzee(dice):
	if most_frequent(dice, [])[1] == 5:
		return True

def check_fullhouse(dice):
	a = dice[0]
	b = '-'
	count1 = 0
	count2 = 0
	for i in dice:
		if i == a:
			count1 += 1
		elif b == '-':
			b = i
			count2 += 1
		elif i == b:
			count2 += 1
		else:
			pass
	if (count1 == 3 and count2 == 2) or (count1 == 2 and count2 == 3):			
		return True
	else:
		return False

def score(dice, scoreboard, category = '-'):
	dice_score = 0
	while category == '-':
		category = input('What category to score? (enter category as word or number): ')
		if category == 'help':
			print('===')
			for i in scoreboard:
				print("'" + i + "'")
			category = '-'
			print('===')
		elif category not in scoreboard:
			print('Category does not exist... (type help for list of categories): ')
			category = '-'
		elif scoreboard[category] != '-':
			category = '-'
			print('Category already used...')

	if len(category) == 1:
		for i in dice:
			if i == int(category):
				dice_score += i
		return [dice_score, category]
	elif category == 'fullhouse':
		if check_fullhouse(dice):
			for i in dice:
				dice_score += i
		return [dice_score, category]
	elif category == 'random':
		for i in dice:
			dice_score += i
		return [dice_score, category]

def get_score(scoreboard):
	cur_score = 0
	for i in scoreboard:
		cur_score += scoreboard[i]
	return cur_score

def show_scoreboard(scoreboard, cpu_scoreboard):
	print('Category    | Player | CPU')
	for i in scoreboard:
		print(' ' + i + ': ' + (' ' * (13 - len(i))) + str(scoreboard[i]) + (' ' * (7 - len(str(scoreboard[i])))) + str(cpu_scoreboard[i]))

def game(scoreboard, cpu_scoreboard):
	turn_count = 0
	while turn_count < len(scoreboard) - 1:
		print()
		turn_result = turn(scoreboard)
		if len(turn_result[1]) == 1:
			scoreboard[turn_result[1]] = turn_result[0]
		else:
			scoreboard[turn_result[1]] = turn_result[0]
		turn_count += 1
		print()
		cpu_turn_result = cpu_turn(cpu_scoreboard)
		if len(turn_result[1]) == 1:
			cpu_scoreboard[cpu_turn_result[1]] = cpu_turn_result[0]
		else:
			cpu_scoreboard[cpu_turn_result[1]] = cpu_turn_result[0]
		show_scoreboard(scoreboard, cpu_scoreboard)
	print('Player Score: ' + str(get_score(scoreboard)))
	print('CPU Score: ' + str(get_score(cpu_scoreboard)))

def new_scoreboard():
	return {'1':'-', '2':'-', '3':'-', '4':'-', '5':'-', '6':'-', 'fullhouse':'-', 'random':'-', 'yahtzee': 0}

game(new_scoreboard(), new_scoreboard())




