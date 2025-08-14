import colorama
from colorama import Fore, Style
from textblob import TextBlob

# Init colored output
colorama.init(autoreset=True)

print(f"{Fore.CYAN}👋🎉 Welcome to Sentiment Spy! 🕵️")

# Ask name
user_name = input(f"{Fore.MAGENTA}Please enter your name: {Style.RESET_ALL}").strip() or "Mystery Agent"

# Store history as (text, polarity, label)
history = []

print(
    f"\n{Fore.CYAN}Hello, Agent {user_name}!\n"
    f"Type a sentence and I will analyze its sentiment. 🔎\n"
    f"Type {Fore.YELLOW}'history'{Fore.CYAN} to see past results, "
    f"{Fore.YELLOW}'reset'{Fore.CYAN} to clear, or {Fore.YELLOW}'exit'{Fore.CYAN} to quit.\n"
)

while True:
    text = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()
    if not text:
        print(f"{Fore.RED}Please type something or use a command.")
        continue

    cmd = text.lower()
    if cmd == "exit":
        print(f"\n{Fore.BLUE}🚪 Exiting Sentiment Spy. Farewell, Agent {user_name}! 🏁")
        break

    if cmd == "reset":
        history.clear()
        print(f"{Fore.CYAN}🎉 History cleared.")
        continue

    if cmd == "history":
        if not history:
            print(f"{Fore.YELLOW}No conversation history yet.")
        else:
            print(f"{Fore.CYAN}📜 Conversation History:")
            for i, (t, p, lbl) in enumerate(history, 1):
                color = Fore.GREEN if lbl == "Positive" else Fore.RED if lbl == "Negative" else Fore.YELLOW
                emoji = "😊" if lbl == "Positive" else "😢" if lbl == "Negative" else "😐"
                print(f"{i}. {color}{emoji} {t} (Polarity: {p:.2f}, {lbl})")
        continue

    # Analyze sentiment
    polarity = TextBlob(text).sentiment.polarity  # -1.0 .. 1.0
    if polarity > 0.25:
        label, color, emoji = "Positive", Fore.GREEN, "😊"
    elif polarity < -0.25:
        label, color, emoji = "Negative", Fore.RED, "😢"
    else:
        label, color, emoji = "Neutral", Fore.YELLOW, "😐"

    history.append((text, polarity, label))
    print(f"{color}{emoji} {label} sentiment detected! (Polarity: {polarity:.2f})")
