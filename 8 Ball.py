import random
# 8 ball generator

def eight_ball():
    responses = [
        "Yes - definitely.",
        "It is decidedly so.",
        "Without a doubt.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not to tell you.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    return random.choice(responses)

def main():
    while True:
        question = input("Ask the Magic 8 Ball a question (or 'quit'): ")
        if question.lower() == "quit":
            print("Goodbye!")
            break
        print("Magic 8 Ball says:", eight_ball())

if __name__ == "__main__":
    main()
