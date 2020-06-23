#  Python code for Ten Games for the Circuit Playground Express
#    by Rick Leander
#  Copyright (c) 2020 Rick Leander All rights reserved
#  Buy the book at https://www.amazon.com/author/rleander
#
# Battleships

import random

# globals

board1 = []
board2 = []
ships = []


#------------------
#  game setup functions

#  clear the board

def clear_board():
  board = []
  for i in range (11):
    row = []
    for itm in range(11):
      row.append(0)
    board.append(row)
  return board

# check to see if horizontal space is free

def check_horizontal(x, y, n):
  if x + n > 10:
    return 0
  i = x
  while i < x + n:
    if board1[i][y] > 0:
      return 0
    i = i + 1
  return 1

# check to see if vertical space is free

def check_vertical(x, y, n):
  if y + n > 10:
    return 0
  j = y
  while j < y + n:
    if board1[x][j] > 0:
      return 0
    j = j + 1
  return 1

#  add ship horizontally

def add_horizontal(id, x, y, n):
  i = x
  while i < x + n:
    board1[i][y] = id
    i = i + 1

# add ship vertically

def add_vertical (id, x, y, n):
  j = y
  while j < y + n:
    board1[x][j] = id
    j = j + 1

# add ships

def add_ship(name, n):
  ships.append ([name, n])
  id = len(ships) - 1
 
  success = 0
  while success == 0:
    dir = random.randint(1, 2)
    x = random.randint(1, 10)
    y = random.randint(1, 10)
    if dir == 1:
      if check_horizontal(x, y, n) == 1:
        add_horizontal(id, x, y, n)
        success = 1
    else:
      if check_vertical(x, y, n) == 1:
        add_vertical(id, x, y, n)
        success = 1

# [print board 1 - for debuggung

def print_board1():
  print()
  print ('Board1')
  i = 1
  while i < 11:
    print (board1[i])
    i = i + 1
  print()
  print ('ships:')
  print(ships)
  print()

# set up the boards

def setup_boards():
  global board1, board2, ships

  board1 = clear_board()
  board2 = clear_board()
  ships = [['not used', 0]]

  add_ship('carrier', 5)
  add_ship('battleship', 4)
  add_ship('destroyer', 3)
  add_ship('submarine', 3)
  add_ship('cruiser', 2)

#-----------------
# game play functions

# print board 2

def print_board2():
  letters = ' ABCDEFGHIJ'

  print ('   1 2 3 4 5 6 7 8 9 10')
  for i in range(1, 11):
    txt = letters[i] + ': '
    for j in range(1, 11):
      if board2[i][j] == 0:
        txt = txt + '. '
      elif board2[i][j] < 0:
        txt = txt + '* '
      elif board2[i][j] > 0: 
        txt = txt + 'O '
    print(txt)
  print ()

# parse command

def get_coords(cmd):
  x = -1
  y = -1
  part1 = ''
  part2 = ''

  if len(cmd) < 2:
    return [x, y]

  part1 = cmd[0]
  part2 = cmd[1]
  if part2 < '1' or part2 > '9':
    return [x, y]

  if len(cmd) > 2:
    part2 = part2 + cmd[2]
    if part2 != '10':
      return [x, y]

  if part1 < 'A' or part1 > 'J':
    return [x, y]

  x = ord(part1) - ord('A') + 1
  y = int(part2)
  return [x, y]

#  check the shot and mark boards

def check_hit (x, y):
  if board2[x][y] != 0:
    print ('You already hit that square')
    return 0

  if board1[x][y] == 0:
    print ('missed')
    board2[x][y] = -1
    return 0

# if we get here we have a hit

  board2[x][y] = 1
  id = board1[x][y]
  ships[id][1] = ships[id][1] - 1
  if ships[id][1] == 0:
    print ('You sunk my ' + ships[id][0])
  else:
    print ('You hit my ' + ships[id][0])
  return 1

#  play the game

def play_game():
  setup_boards()

  tries = 0
  hits = 0
  while hits < 17:
    print_board2()

    x = -1
    y = -1
    while x < 0 or y < 0:  
      cmd = input('>>')
      if cmd == 'exit':
        return

      [x, y] = get_coords(cmd)
      if x < 0 or y < 0:
        print('what?')

    result = check_hit(x, y)
    hits = hits + result
    tries = tries + 1

  if hits >= 17:
    print ('Congratulations - you sunk my fleet')
    print ('It took you ' + str(tries) + ' shots')


# print help messages

def show_help():
  print ('Welcome to Battleship')
  print ()
  print ('This is a single player version of the battleship game - ')
  print ('you against the computer.')
  print('The computer will arrange its ships on a 10 by 10 grid ')
  print ('and you must find and sink the ships.')
  print ()
  print ('The computer will deploy the following ships:')
  print ('  Carrier: 5 squares')
  print ('  Battleships: 4')
  print ('  Cruisers: 3')
  print ('  Submarine: 3')
  print ('  Destroyer: 2')
  print ('')
  print ('Enter coordinates using letters A through J followed by numbers 1 through 10.')
  print ('For example, A1 would hit the square on the first row, first column,')
  print ('C6 would hit the square on the third row, sixth column.')
  print ('Continue to fire your shots until you sink all of the ships.')
  print()
  print ('This code was published in the book ')
  print('Ten Games for the Circuit Playground Express')
  print ('  by Rick Leander.')
  print()
  print ('If you enjoy this game, please purchase the book from')
  print ('https://www.amazon.com/author/rleander')
  print()



# main loop

print ('Welcome to Battleships')
print()

cmd = ''
while cmd != 'exit':
  print ()
  print ("Type 'new' for new game, 'help' for help or 'exit' to quit")
  cmd = input('?') 
  if cmd == 'help':
    show_help()
  if cmd == 'new':
    play_game()

 