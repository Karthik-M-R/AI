"""
THE COMPLETE GENERATORS GUIDE

Covers: yield, next(), infinite generators, .send(), and yield from.
"""

# 1. BASIC GENERATOR & NEXT() 
def color_sequence():
    """
    A generator is a function that 'yields' values one by one 
    instead of returning them all at once.
    """
    print("--- Start of Generator ---")
    yield "Red"    # Execution pauses here after the first next()
    yield "Green"  # Execution resumes here on the second next()
    yield "Blue"   # Execution resumes here on the third next()

# Usage:
gen = color_sequence()
print(next(gen)) # Prints "Red"
print(next(gen)) # Prints "Green"
# 


# 2. INFINITE GENERATORS 
def infinite_id_generator():
    """
    Because generators are 'lazy', they can run forever 
    without filling up your RAM.
    """
    user_id = 1000
    while True:
        yield user_id
        user_id += 1

# Usage:
id_gen = infinite_id_generator()
print(f"User ID: {next(id_gen)}") # 1000
print(f"User ID: {next(id_gen)}") # 1001


# 3. SENDING VALUES INTO GENERATORS 
def smart_thermometer():
    """
    Using '.send()', we can pass data back into the generator
    where the yield statement is currently paused.
    """
    temp = 20 # Starting temperature
    while True:
        # Execution pauses at yield. When .send(X) is called, 
        # X is assigned to the 'adjustment' variable.
        adjustment = yield f"Current Temp: {temp}°C"
        
        if adjustment is not None:
            temp += adjustment
        else:
            temp += 1 # Default increase

# Usage:
therm = smart_thermometer()
print(next(therm))        # MUST "prime" the generator first
print(therm.send(5))      # Jumps from 20 to 25
print(therm.send(-10))    # Jumps from 25 to 15


# 4. YIELD FROM (Delegation) 
def sub_task():
    yield "Step 2: Scrape Data"
    yield "Step 3: Clean Data"

def main_workflow():
    yield "Step 1: Connect to Source"
    yield from sub_task() # 'yield from' sucks all yields out of sub_task
    yield "Step 4: Save to CSV"

# Usage:
print("\nRunning Workflow:")
for step in main_workflow():
    print(step)
# 


# 5. CLOSING GENERATORS (Topic 56)
def temporary_gen():
    try:
        yield "Processing..."
        yield "Still working..."
    finally:
        print("Generator has been manually closed.")

# Usage:
t_gen = temporary_gen()
print(next(t_gen))
t_gen.close() # Forces the generator to stop immediately


# 6. PRACTICAL COMBO: Generator + Loop Fallback
def find_item(target, items):
    for item in items:
        if item == target:
            yield f"Found {target}!"
            break
    else:
        # Runs if 'break' was never hit
        yield f"{target} not found in the list."

# Usage:
search = find_item("Gold", ["Iron", "Silver", "Copper"])
print(next(search)) # Gold not found...