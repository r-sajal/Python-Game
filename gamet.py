from tkinter import *
import numpy as np
import pygame
import sys
import math



window = Tk()
window.title("Connect Four")
window.geometry('700x500+150+100')

img = PhotoImage(file='C:/Users/Sajal/Desktop/bird.png')
img = img.subsample(2)
Label(window, image=img).place(x=0,y=0,relwidth = 1)
Label(window,text = 'Welcome To Connect4',font=('sans sherif bold', 25),bg = 'black' , fg = 'white').place(x = 220 , y = 20)
Label(window, text='Player1',font=('sans sherifbold', 19),bg = 'black' , fg = 'red').place(x=180, y=180)
player1_entry = Entry(window,width=20,font=('Courier New bold italic' , 14),bg = 'black' , fg = 'red',	highlightthickness = '1' , highlightcolor = 'red')
player1_entry.focus_set()
player1_entry.place(x=350, y=185)
#player1 = player1_entry.get()
Label(window, text='Player2', font=('sans sherif', 19),bg = 'black' , fg = 'green').place(x=180, y=250)
player2_entry = Entry(window, width=20 ,font=('Courier New bold italic' , 14),	highlightthickness = '1' , highlightcolor = 'green',bg = 'black' , fg = 'green')
player1_entry.bind('<Return>', lambda event :player2_entry.focus_set())

player2_entry.place(x=350, y=255)
#player2 = player2_entry.get()



def game():

    player1 = player1_entry.get()
    player2 = player2_entry.get()
    print(player1)
    window.destroy()

    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (0, 255, 0)

    ROW_COUNT = 6
    COLUMN_COUNT = 7

    def create_board():
        board = np.zeros((6, 7))
        return board

    def drop_piece(board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(board, col):
        return board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    def print_board(board):
        print(np.flip(board, 0))

    def winning_move(board, piece):
        # horizontal
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True

            # check vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

            # diagonal positive
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

            # diagonal negative
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True

    def draw_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    pygame.init()
    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)
    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 50)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # Player 1
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            #print(globals()['player1'])
                            label = myfont.render((player1 + " Wins :) "), 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                # Player 2
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render(player2+" Wins :) ", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                turn += 1
                turn = turn % 2
                print_board(board)
                draw_board(board)

                if game_over:
                    pygame.time.wait(3000)

Button(window, text='Submit', command= game,font=('sans sherif', 16),bg = 'black' , fg = 'white').place(x=350, y=325)

window.mainloop()

