#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from random import randint

class Dice:

	def __init__(self):
		self.val = None
		self.state = 0


class Yahtzee:

	upper_block = ['Aces',		# Category of scoring in the upper block
					'Twos',
					'Threes',
					'Fours',
					'Fives',
					'Sixes']

	lower_block = ['Three Of A Kind',	# Category of scoring in the lower block
					'Four Of A Kind',
					'Full House',
					'Small Straight',
					'Large Straight',
					'Yahtzee',
					'Chance']

	max_turn	= 13

	def __init__(self, master):

		self.master = master

		self.num_of_round = 1
		self.num_of_roll = 0

		self.score = []
		self.total_score = 0

		self.dice = [Dice(),Dice(),Dice(),Dice(),Dice()]

		self.button_roll_dice = Button(master, width=10, text='Roll dice', fg="BLUE", command=self.roll_dice)
		self.button_roll_dice.grid(row=0,column=0,columnspan=2)

		# Checkbox keeping dices
		self.frame_checkbox = Frame(master)
		self.chk_group = []
		self.keep_dice = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
		self.keep_label = Label(self.frame_checkbox, width=5, text='Keep: ')
		self.keep_label.grid(row=2)
		for i in range(5):
			self.chk_group.append(Checkbutton(self.frame_checkbox, text=str(i+1), state=DISABLED, variable=self.keep_dice[i]))
			self.chk_group[i].grid(row=2,column = i+1)
		self.frame_checkbox.grid(row=2,columnspan=2)

		# Scoring button
		self.frame_score_button = Frame(master)
		self.button_upper_block = []
		for i, category in enumerate(self.upper_block):
			self.button_upper_block.append(Button(self.frame_score_button, text=category, fg="BLUE", state=DISABLED, width=15, command=lambda option=i: self.calculate_score(option, False)))
			self.button_upper_block[i].grid(row=i)
		self.button_lower_block = []
		for i, category in enumerate(self.lower_block):
			self.button_lower_block.append(Button(self.frame_score_button, text=category, fg="BLUE", state=DISABLED, width=15, command=lambda option=category: self.calculate_score(option, True)))
			self.button_lower_block[i].grid(row=i, column=1)
		self.frame_score_button.grid(row=3,columnspan=2)

		self.button_test = Button(master, text='Test', fg="BLUE", state=NORMAL, command=self.count_pip)
		self.button_test.grid(row=4,column=0)

		self.new_round()


	def init_widgets(self):
		for i in self.chk_group:
			i.config(state=DISABLED)
			i.deselect()

		for i in self.button_upper_block:
			i.config(state=DISABLED)

		for i in self.button_lower_block:
			i.config(state=DISABLED)


	def calculate_score(self, option, is_lower_block):

		score = 0
		frequency = self.count_pip()

		if not is_lower_block:
			# Upper Block scoring
			print('{} is chosen!'.format(self.upper_block[option]))
			score = frequency[option] * (option+1)

		else:
			# Lower Block scoring
			print('{} is chosen!'.format(option))
			if option == self.lower_block[0] or option == self.lower_block[1] or option == self.lower_block[6]: score = sum([x.val for x in self.dice])
			elif option == self.lower_block[2]: score = 25
			elif option == self.lower_block[3]: score = 30
			elif option == self.lower_block[4]: score = 40
			elif option == self.lower_block[5]: score = 50
			else: score = 0

		self.total_score += score
		print('Score: {} / Total score: {}'.format(score, self.total_score))

		self.new_round()


	def new_round(self):
		
		self.num_of_roll = 0
		self.init_widgets()
		for i in self.dice:
			i.state = 0
			i.val = None

		self.button_roll_dice.config(state=NORMAL)
		print('\n----------------' + 'Round: ' + str(self.num_of_round) + '----------------')

		self.num_of_round += 1


	def roll_dice(self):
		
		self.num_of_roll += 1

		if self.num_of_roll < 4:
			for i, j in enumerate(self.dice):
				j.state = self.keep_dice[i].get()
				if not j.state:	self.dice[i].val = randint(1,6)

			print('roll #' + str(self.num_of_roll) + ': ' + str([i.val for i in self.dice]))

			if self.num_of_roll == 3: 
				self.button_roll_dice.config(state=DISABLED)
				for i in self.chk_group:
					i.config(state=DISABLED)

			for i in self.chk_group:
				i.config(state=NORMAL)
				i.deselect()

		self.enable_button()


	def enable_button(self):

		frequency = self.count_pip()
		dice_pip = [x.val for x in self.dice]

		for i, button in enumerate(self.button_upper_block):
			if frequency[i]: button.config(state=NORMAL)
			else: button.config(state=DISABLED)

		for i in self.button_lower_block:
			i.config(state=DISABLED)

		if 5 in frequency: self.button_lower_block[0].config(state=NORMAL), self.button_lower_block[1].config(state=NORMAL), self.button_lower_block[5].config(state=NORMAL)
		if 4 in frequency: self.button_lower_block[0].config(state=NORMAL), self.button_lower_block[1].config(state=NORMAL)
		if 3 in frequency: self.button_lower_block[0].config(state=NORMAL)
		if frequency.count(2) == 1 and frequency.count(3) == 1: self.button_lower_block[2].config(state=NORMAL)	# Full house
		if list(set(dice_pip)) in [[1,2,3,4,5],[2,3,4,5,6]]: self.button_lower_block[4].config(state=NORMAL), self.button_lower_block[3].config(state=NORMAL)	# Large straight
		if list(set(dice_pip)) in [[1,2,3,4],[2,3,4,5],[3,4,5,6]]: self.button_lower_block[3].config(state=NORMAL)	# small straight


	def count_pip(self):
		return [[x.val for x in self.dice].count(i+1) for i in range(6)]
		

root = Tk()
root.wm_title("Yahtzee!!")
root.resizable(width=False, height=False)
app = Yahtzee(root)
root.mainloop()