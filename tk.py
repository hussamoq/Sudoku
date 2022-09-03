"""
A simple program that solves sudoku problems
"""
import threading
import time
import tkinter as tk
from tkinter import messagebox

buttons_array = [] #Array of buttons corresponds to the grid
grid = [] #The array grid that corresponds to the buttons
is_solved = False #Checks wether grid was solved
delay = 0.2 #Delay time to change each cell 
for i in range(9):
    buttons_array.append([])
    grid.append([0] * 9)
selected_coordinate = [-1, -1] #User current selected cell y and x coordinates ([0] = y, [1] = x)

solutions = [] #A list of grids to store solutions
random_grids = [
    [[0, 0, 5, 3, 0, 0, 0, 0, 0], 
    [8, 0, 0, 0, 0, 0, 0, 2, 0], 
    [0, 7, 0, 0, 1, 0, 5, 0, 0], 
    [4, 0, 0, 0, 0, 5, 3, 0, 0], 
    [0, 1, 0, 0, 7, 0, 0, 0, 6], 
    [0, 0, 3, 2, 0, 0, 0, 8, 0], 
    [0, 6, 0, 5, 0, 0, 0, 0, 9], 
    [0, 0, 4, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 9, 7, 0, 0]],

    [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 8, 5],
    [0, 0, 1, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 7, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 1, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 7, 3],
    [0, 0, 2, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 9]]
]

def set_coordinates(y, x):
    """
    Sets cell that user selected
    """
    selected_coordinate[0] = y
    selected_coordinate[1] = x
        
def on_window_destruction():
    global window
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        window.destroy()

def solve_sudoku():
    """
    Solves sudoku
    """
     
    if check_grid() == False:
        messagebox.showerror('Invalid grid', 'Could not solve: input grid already invalid')
        return

    global buttons_array
    global grid
    global solutions
    global is_solved

    def check_validity(grid):
        """
        Checks if sudoku is solved (No exsiting empty cells)
        And if this is a new solution
        """
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return False

        if grid in solutions:
            return False

        return True

    def possible(y, x, grid, num):
        for i in range(9):
            if grid[y][i] == num:
                return False
        for i in range(9):
            if grid[i][x] == num:
                return False
    
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3

        for i in range(3):
            for j in range(3):
                if grid[i + y0][j + x0] == num:
                    return False
        return True
        
    def solve(buttons_array, grid):
        global is_solved
        if not is_solved:
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        for n in range(1, 10):
                            if possible(i, j, grid, n):
                                grid[i][j] = n
                                buttons_array[i][j]['text'] = grid[i][j]
                                time.sleep(delay)
                                print(f'[{i}][{j}] = {buttons_array[i][j]["text"]}')
                                solve(buttons_array, grid)
                                if is_solved:
                                    break
                                grid[i][j] = 0
                                buttons_array[i][j]['text'] = str(0)
                        return
        if check_validity(grid):
            print(grid)
            solutions.append(grid)
            is_solved = True

    print('Solving...')
    is_solved = False
    solve(buttons_array, grid)
    if not is_solved:
        messagebox.showerror('No solutions', 'No solution found')
 
solve_grid_thread = threading.Thread(target=solve_sudoku) #Seperate thread for sudoku 

choice = 0
def generate_grid(): #Generates grid sequantially 
    global choice
    global grid
    if choice == len(random_grids):
        choice = 0
    grid = random_grids[choice]
    choice += 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            buttons_array[i][j]['text'] = str(grid[i][j])

def change_delay():
    global delay

    def change(event):
        global delay
        try:
            value = float(delay_entry.get())
        except:
            prompt.destroy()
        else:
            delay = value
        
        prompt.destroy()

    prompt = tk.Tk()
    delay_label = tk.Label(master=prompt, text='Choose new delay:')
    delay_label.grid(row=0, column=0, sticky='nw')
    delay_entry = tk.Entry(master=prompt)
    delay_entry.grid(row=0, column=1, sticky='nw')

    delay_entry.bind('<Return>', change)

def increment_cell():
    if selected_coordinate[0] == -1 or selected_coordinate[1] == -1: #If user has not selected a button yet then abort
        return
    global grid
    global buttons_array
    y = selected_coordinate[0]
    x = selected_coordinate[1]
    if grid[y][x] == 9:
        grid[y][x] = 0
    else:
        grid[y][x] += 1

    buttons_array[y][x]['text'] = str(grid[y][x])

def decrement_cell():
    if selected_coordinate[0] == -1 or selected_coordinate[1] == -1:
        return
    global grid
    global buttons_array
    y = selected_coordinate[0]
    x = selected_coordinate[1]
    if grid[y][x] == 0:
        grid[y][x] = 9
    else:
        grid[y][x] -= 1

    buttons_array[y][x]['text'] = str(grid[y][x])

def check_grid():
    """
    This function is called by the user to check if his grid right so far
    """
    global grid

    def check(y, x, grid):
        if grid[y][x] == 0:
            return
        store = grid[y][x]
        grid[y][x] = 0
        for i in range(9): #Check column
            if grid[y][i] == store:
                grid[y][x] = store
                return False
        for i in range(9): #Check row
            if grid[i][x] == store:
                grid[y][x] = store
                return False

        x0 = (x // 3) * 3
        y0 = (y // 3) * 3

        for i in range(3):
            for j in range(3):
                if grid[i + y0][j + x0] == store:
                    grid[y][x] = store
                    return False
        grid[y][x] = store
        return True

    for y in range(9):
        for x in range(9):
            if check(y, x, grid) == False:
                messagebox.showerror('INVALID', 'This grid is invalid.')
                return False

    messagebox.showinfo('VALID', 'This grid is valid.')
    return True

def handle_threading():
    solve_grid_thread = threading.Thread(target=solve_sudoku)
    solve_grid_thread.start()

if __name__ == '__main__':
    #creates window
    window = tk.Tk()
    window.geometry('500x500')
    window.title('Sudoku Solver')
    window.protocol('WM_DELETE_WINDOW', on_window_destruction)

    #configuration for each frame
    for i in range(3):
        window.rowconfigure(i, weight=1, minsize=30)
        window.columnconfigure(i, weight=1, minsize=30)

    #frame 3x3 confirguration
    for r_frame in range(3):
        for c_frame in range(3):
            frame = tk.Frame(master=window, borderwidth=3, relief=tk.GROOVE)
            frame.grid(row=r_frame, column=c_frame, sticky='nsew', padx=2, pady=2)

            #cells inside each frame configuration
            for i in range(3):
                frame.rowconfigure(i, weight=1, minsize=20)
                frame.columnconfigure(i, weight=1, minsize=20) 
            
            #3x3 buttons inside each frame 
            for r_button in range(3):
                for c_button in range(3):
                    row = r_button + (r_frame * 3)
                    column = (c_button + (c_frame * 3)) 
                    button = tk.Button(master=frame, text='0', command=(lambda r=row, c=column : set_coordinates(r, c)))
                    button.grid(row=r_button, column=c_button, sticky='nsew', padx=1, pady=1)
                    buttons_array[r_button + (r_frame * 3)].append(button)

    solve_sudoku_thread = threading.Thread(target=solve_sudoku)

    solve_button = tk.Button(master=window ,text='Solve!', width=10, height=2, fg='red', command=handle_threading)
    solve_button.grid(row=3, column=0, sticky='nw', padx=3, pady=1)

    check_button = tk.Button(master=window, text='Check', width=10, height=2, fg='blue', command=check_grid)
    check_button.grid(row=3, column=0, sticky='ne')

    generate_button = tk.Button(master=window, text='Generate grid', width=10, height=2, fg='green', command=generate_grid)
    generate_button.grid(row=3, column=1, sticky='w', pady=1)

    delay_button = tk.Button(master=window, text='Delay', width=10, height=2, fg='purple', command=change_delay)
    delay_button.grid(row=3, column=1, sticky='e', pady=1)

    plus_button = tk.Button(master=window, text='+', fg='black',width=6,height=2, command=increment_cell)
    plus_button.grid(row=3, column=2, sticky='nw', padx=2, pady=1)

    minus_button = tk.Button(master=window, text='-', fg='black', width=6, height=2, command=decrement_cell)
    minus_button.grid(row=3, column=2, sticky='ne', padx=2, pady=1)

    try:
        with open('enterGridHere.txt', 'r') as sudokus:  #Read grid from text file
            for i, line in enumerate(sudokus.readlines()):
                for j, num in enumerate(line.split()):
                    if num.isnumeric():
                        grid[i][j] = int(num)
                        buttons_array[i][j]['text'] = num     
    except FileNotFoundError:
        messagebox.showerror('File Error', f'Exception: File could not be open')
    except Exception as e:
        messagebox.showerror('File Error', 'Error reading file')

    window.mainloop()
