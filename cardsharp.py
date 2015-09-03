#! /usr/bin/env python2.7

import npyscreen, sys

VALUES = "A234567890JQK"[::-1]
SUITS = "SHCD"

class Card:
  def __init__(self, value, suit):
    self.value = value.upper()
    self.suit = suit.upper()
    self.visible = True

  def show(self, boolean):
    self.visible = boolean

  def __str__(self):
    prefix = "*" if not self.visible else ""
    return "{}{}{}".format(prefix, self.value, self.suit) 

  def __cmp__(self, other):
    if self.value in VALUES and other.value in VALUES:
      if not self.value == other.value:
        return cmp(VALUES.index(self.value), VALUES.index(other.value))
      else:
        if self.suit in SUITS and other.suit in SUITS:
          return cmp(SUITS.index(self.suit), SUITS.index(other.suit))
        else:
          return -1


class HiddenColorGrid(npyscreen.SimpleGrid):
  def custom_print_cell(self, actual_cell, cell_display_value):
    if cell_display_value.startswith("*"):
      actual_cell.color = 'DANGER'
    else:
      actual_cell.color = 'DEFAULT'


class ActionControllerCard(npyscreen.ActionControllerSimple):
  def create(self):
    self.add_action('(?i)^:([{}][{}]\s?)+$'.format(VALUES, SUITS), self.remove_card, False)
    self.add_action('(?i)^:u$', self.undo, False)
    self.add_action('(?i)^:q$', self.quit, False)
    self.add_action('(?i)^:reset$', self.reset, False)

  def reset(self, command_line, control_widget, live):
    self.parent.value.create()
    self.updateDisplay('reset')

  def remove_card(self, command_line, control_widget, live):
    command_line = command_line[1:]
    cards = command_line.split(' ')
    # Get all our cards and remove each one.
    for obj in cards:
      card = Card(obj[0], obj[1])
      self.parent.value.removeCard(card)

    self.updateDisplay("remove " + command_line)

  def undo(self, command_line, control_widget, live):
    self.parent.value.undo()
    self.updateDisplay('undo')

  def updateDisplay(self, status):
    self.parent.wStatus2.value = status
    self.parent.wStatus2.display()
    self.parent.wMain.set_grid_values_from_flat_list(self.parent.value.showCards(), max_cols=4)
    self.parent.wMain.display()

  def quit(self, command_line, control_widget, live):
    sys.exit(0)


class DataControllerCard:

  def create(self):
    self.cards = self.gen_cards();
    self.cards.sort()
    self.discard = [];

  def gen_cards(self):
    return [Card(v, s) for s in SUITS for v in VALUES]

  def removeCard(self, card):
    try:
      index = self.cards.index(card)
      self.cards[index].show(False)
      self.discard.append(card)
    except:
      return

  def undo(self):
    if len(self.discard) > 0:
      card = self.discard.pop()
      self.cards[self.cards.index(card)].show(True)

  def showCards(self):
    return self.cards


class AppWindow(npyscreen.FormMuttActiveTraditional):
  ACTION_CONTROLLER = ActionControllerCard
  #TODO DATA_CONTROLER is bad spelling!
  DATA_CONTROLER = DataControllerCard
  MAIN_WIDGET_CLASS = HiddenColorGrid


class DeckrApp(npyscreen.NPSApp):
  def main(self):
    F = AppWindow()
    F.value.create()
    F.wMain.set_grid_values_from_flat_list(F.value.showCards(), max_cols=4)
    F.edit()


if __name__ == '__main__':
  DA = DeckrApp()
  DA.run()
