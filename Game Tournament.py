def video_game_tournament_batch():
    print("Welcome to the Video Game Tournament!")
    print("Enter 'quit' as your name anytime to exit.\n")

    while True:
        # --- Participant Info ---
        name = input("Enter your name: ").strip()
        if name.lower() == "quit":
            print("Thank you for participating! Goodbye!")
            break
        if not name or any(char.isdigit() for char in name):
            print("Invalid name. Please enter a valid name without numbers.\n")
            continue

        # Age
        try:
            age = int(input("Enter your age: ").strip())
            if age < 0 or age > 120:
                print("Invalid age. Please enter a number between 0 and 120.\n")
                continue
        except ValueError:
            print("Invalid input. Please enter a numeric age.\n")
            continue

        # VIP
        vip_input = input("Are you a VIP member? (yes/no): ").strip().lower()
        if vip_input not in ["yes", "no"]:
            print("Invalid input for VIP status.\n")
            continue
        is_vip = vip_input == "yes"

        # Adult supervision
        adult_input = input(
            "Are you accompanied by an adult? (yes/no): ").strip().lower()
        if adult_input not in ["yes", "no"]:
            print("Invalid input for adult supervision.\n")
            continue
        has_adult_supervision = adult_input == "yes"

        # Parental consent
        parent_input = input(
            "Do you have parental consent? (yes/no): ").strip().lower()
        if parent_input not in ["yes", "no"]:
            print("Invalid input for parental consent.\n")
            continue
        has_parental_consent = parent_input == "yes"

        # --- Games Input ---
        games_input = input(
            "Enter your games and ratings (format: Game1:E, Game2:T, Game3:M): ").strip()
        game_pairs = [g.strip() for g in games_input.split(",")]

        allowed_games = []
        denied_games = []

        for pair in game_pairs:
            if ":" not in pair:
                print(f"Invalid format for '{pair}', skipping this game.")
                continue

            game_name, game_rating = [x.strip() for x in pair.split(":", 1)]
            game_rating = game_rating.upper()

            if game_rating not in ["E", "T", "M"]:
                print(f"Invalid rating for {game_name}, skipping this game.")
                continue

            # --- Eligibility Check ---
            allowed = False
            reason = ""

            if is_vip:
                allowed = True
            elif age >= 18:
                allowed = True
            elif 13 <= age < 18:
                if game_rating in ["E", "T"] and has_parental_consent:
                    allowed = True
                else:
                    reason = "Parental consent required for Teen-rated games or higher."
            elif age < 13:
                if game_rating == "E" and has_adult_supervision:
                    allowed = True
                else:
                    reason = "Adult supervision required or too young for this game."

            # --- Add to summary lists ---
            if allowed:
                allowed_games.append(game_name)
            else:
                denied_games.append((game_name, reason))

        # --- Print Summary ---
        if allowed_games:
            print(f"\n{name}, you are allowed to play: {', '.join(allowed_games)}")
        if denied_games:
            for game, reason in denied_games:
                print(f"Access denied for {game}: {reason}")
        print("\n" + "-"*50 + "\n")


# Run the program
video_game_tournament_batch()
