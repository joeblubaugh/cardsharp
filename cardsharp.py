#! /usr/bin/env python2.7

import npyscreen, sys

VALUES = "A234567890JQK"[::-1]
SUITS = "SHCD"

class Card:
  def __init__(self, value, suit):
    self.value = value
    self.suit = suit

  def __str__(self):
    return "{}{}".format(self.value, self.suit)

  def __cmp__(self, other):
    if self.value in VALUES and other.value in VALUES:
      if not self.value == other.value:
        return cmp(VALUES.index(self.value), VALUES.index(other.value))
      else:
        if self.suit in SUITS and other.suit in SUITS:
          return cmp(SUITS.index(self.suit), SUITS.index(other.suit))
        else:
          return 0


class ActionControllerCard(npyscreen.ActionControllerSimple):
  def create(self):
    self.add_action('^:([{}][{}]\s?)+$'.format(VALUES, SUITS), self.remove_card, False)
    self.add_action('^:u$', self.undo, False)
    self.add_action('^:q$', self.quit, False)
    self.add_action('^:reset$', self.reset, False)

  def reset(self, command_line, control_widget, live):
    self.parent.value.create()
    self.updateDisplay('reset')

  def remove_card(self, command_line, control_widget, live):
    # Get all our cards and remove each one.
    card = Card(command_line[1], command_line[2])
    self.parent.value.removeCard(card)
    self.updateDisplay("remove " + str(card))

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
    if card in self.cards:
      self.cards.remove(card)
      self.cards.sort()
      self.discard.append(card)

  def undo(self):
    if len(self.discard) > 0:
      self.cards.append(self.discard.pop())
      self.cards.sort()

  def showCards(self):
    return self.cards


class AppWindow(npyscreen.FormMuttActiveTraditional):
  ACTION_CONTROLLER = ActionControllerCard
  #TODO DATA_CONTROLER is bad spelling!
  DATA_CONTROLER = DataControllerCard
  MAIN_WIDGET_CLASS = npyscreen.SimpleGrid


class DeckrApp(npyscreen.NPSApp):
  def main(self):
    F = AppWindow()
    F.value.create()
    F.wMain.set_grid_values_from_flat_list(F.value.showCards(), max_cols=4)
    F.edit()


if __name__ == '__main__':
  DA = DeckrApp()
  DA.run()
