#main.py
from orchestrator.orchestrator import setup, management, check
def main():
    print("Welcome to the application!")

    while True:
        action = input("Type a command (setup, management, check), or 'exit' to quit: ").strip()

        if action == 'setup':
            print('Running setup...')
            setup()
        elif action == 'management':
            print('Running client management...')
            management()
        elif action == 'check':
            print('Running check...')
            check()
        elif action == 'exit':
            print('Exiting...')
            break
        else:
            print('Invalid command. Please try again.')

if __name__ == '__main__':
    main()

