try:
    num = int(input("Enter a number: "))
    print(num)
except ValueError:
    print("Please enter a valid integer.")