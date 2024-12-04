# import the math module
import math

# define a function to calculate the area of a circle
def circle_area(r):
    area = math.pi * r ** 2
    return area

# ask user for radius input and convert to float
while True:
    x = input("\nEnter the radius [cm]: ")
    
    try:
        x = float(x)
        break
    except:
        print("Invalid input. Please enter a VALID number.")

# print the calculated area
print(f"Area = {circle_area(x):.2f} [cm^2]")