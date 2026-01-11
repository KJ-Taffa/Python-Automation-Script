def ride_eligibility():

    # Initial check for VIP pass
    vip_pass = input(
        "Do you have a VIP pass? (yes/no): ").strip().lower()
    if vip_pass not in ["yes", "no"]:
        print("Invalid input for VIP pass.")
        return

    if vip_pass == "yes":
        print("Access granted.")
        return

    # Weekday check
    weekday = input(
        "What day of the week is it? (e.g., Monday): ").strip().lower()
    if weekday not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        print("Invalid day of the week entered.")
        return
    if weekday in ["wednesday", "monday"]:
        print("Ride is closed.")
        return

    # Height and Weight
    height = float(input("Enter your height in cm: "))
    if height < 0 or height > 300:
        print("Invalid height entered.")
        return
    if height < 140:
        print("You are not tall enough to ride.")
        return

    weight = float(input("Enter your weight in kg: "))
    if weight < 0 or weight > 300:
        print("Invalid weight entered.")
        return

    if weight > 200:
        print("You exceed the weight limit to ride.")
        return

    # Age
    age = int(input("Enter your age: "))
    if age < 0 or age > 120:
        print("Invalid age entered.")
        allowed = False
        return

    if age >= 18:
        print("Access granted.")
        return

    # Wavier, Adult Supervision, Safety Gear
    waiver = input("Do you have a signed waiver? (yes/no): ").strip().lower()
    if waiver not in ["yes", "no"]:
        print("Invalid input for waiver.")
        return

    adult_supervision = input(
        "Are you accompanied by an adult? (yes/no): ").strip().lower()
    if adult_supervision not in ["yes", "no"]:
        print("Invalid input for adult supervision.")
        return

    safety_gear = input(
        "Are you wearing the required safety gear? (yes/no): ").strip().lower()
    if safety_gear not in ["yes", "no"]:
        print("Invalid input for safety gear.")
        return
    # Eligibility based on age groups
    allowed = False

    if 15 <= age < 18 and waiver == "yes" and safety_gear == "yes":
        allowed = True
    elif 12 <= age < 15 and adult_supervision == "yes" and safety_gear == "yes":
        allowed = True

    print("Access granted." if allowed else "Access denied.")


ride_eligibility()
