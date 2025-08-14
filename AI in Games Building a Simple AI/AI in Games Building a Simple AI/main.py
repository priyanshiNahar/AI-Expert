# Tic-Tac-Toe with AI (minimax + difficulty)
# pip install colorama
from colorama import init, Fore, Style
init(autoreset=True)

WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def show(b):
    def c(x):
        if x == 'X':   return Fore.RED + x + Style.RESET_ALL
        if x == 'O':   return Fore.BLUE + x + Style.RESET_ALL
        return Fore.YELLOW + x + Style.RESET_ALL
    print("\n " + " | ".join(c(b[i]) for i in range(3)))
    print(Fore.CYAN + "-----------" + Style.RESET_ALL)
    print(" " + " | ".join(c(b[i]) for i in range(3,6)))
    print(Fore.CYAN + "-----------" + Style.RESET_ALL)
    print(" " + " | ".join(c(b[i]) for i in range(6,9)) + "\n")

def winner(b):
    for a,b1,c in WINS:
        if board[a] == board[b1] == board[c] and not board[a].isdigit():
            return board[a]
    return None

def full(b): return all(not s.isdigit() for s in b)
def moves(b): return [i for i,s in enumerate(b) if s.isdigit()]

def minimax(b, me, opp, turn, depth, alpha, beta):
    w = winner(b)
    if w == me:  return 10 - depth, None
    if w == opp: return depth - 10, None
    if full(b):  return 0, None

    if turn == me:
        best = (-999, None)
        for m in moves(b):
            b[m] = me
            score,_ = minimax(b, me, opp, opp, depth+1, alpha, beta)
            b[m] = str(m+1)
            if score > best[0]: best = (score, m)
            alpha = max(alpha, score)
            if beta <= alpha: break
        return best
    else:
        best = (999, None)
        for m in moves(b):
            b[m] = opp
            score,_ = minimax(b, me, opp, me, depth+1, alpha, beta)
            b[m] = str(m+1)
            if score < best[0]: best = (score, m)
            beta = min(beta, score)
            if beta <= alpha: break
        return best

def ai_move(b, ai, human, difficulty):
    # quick tactical wins/blocks first
    for sym in (ai, human):
        for m in moves(b):
            b[m] = sym
            if winner(b) == sym:
                b[m] = ai
                return
            b[m] = str(m+1)
    # difficulty: easy = first avail, medium = shallow search, hard = full
    if difficulty == "easy":
        b[moves(b)[0]] = ai
    else:
        depth_cap = 2 if difficulty == "medium" else 9
        # shallow minimax by limiting depth via heuristic: convert to temp that locks depth
        def bounded_minimax(bd, me, opp, turn, depth, alpha, beta):
            if depth >= depth_cap:
                return 0, None  # heuristic cut (neutral)
            return minimax(bd, me, opp, turn, depth, alpha, beta)
        score, move = bounded_minimax(b, ai, human, ai, 0, -999, 999) if difficulty!="medium" else \
                      bounded_minimax(b, ai, human, ai, 0, -999, 999)
        b[move] = ai

def ask_move(b):
    while True:
        try:
            m = int(input("Enter your move (1-9): "))
            if 1 <= m <= 9 and b[m-1].isdigit():
                return m-1
        except ValueError:
            pass
        print(Fore.RED + "Invalid move. Try again.")

def game():
    print("Welcome to Tic-Tac-Toe!")
    name = input(Fore.GREEN + "Enter your name: " + Style.RESET_ALL).strip() or "Player"
    board = [str(i) for i in range(1,10)]
    human = input("Do you want to be X or O? ").strip().upper()
    while human not in ("X","O"):
        human = input("Please choose X or O: ").strip().upper()
    ai = "O" if human == "X" else "X"
    difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
    if difficulty not in ("easy","medium","hard"): difficulty = "hard"

    turn = "X"  # X always starts
    while True:
        show(board)
        if winner(board) or full(board): break
        if turn == human:
            board[ask_move(board)] = human
        else:
            print("AI is making its move...")
            ai_move(board, ai, human, difficulty)
        turn = ai if turn == human else human

    show(board)
    w = winner(board)
    if not w:
        print(Fore.YELLOW + "It's a tie!")
    elif w == human:
        print(Fore.GREEN + f"Congrats, {name}! You win.")
    else:
        print(Fore.RED + "AI has won the game!")
    if input("Play again? (yes/no): ").strip().lower() == "yes":
        print()
        game()

if __name__ == "__main__":
    game()
