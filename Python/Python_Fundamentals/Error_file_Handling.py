"""
THE ERROR HANDLING MASTERCLASS

Covers: try/except/else/finally, Custom Exceptions, Raise, and File Handling.
"""

# ---  Creating Custom Exceptions ---
class NegativeNumberError(Exception):
    """Exception raised when a user provides a negative number where not allowed."""
    def __init__(self, message="Numbers must be positive!"):
        self.message = message
        super().__init__(self.message)

# --- . Mini Project: The Secure Divider ---
def secure_divider():
    print("\n--- Welcome to the Secure Divider ---")
    
    filename = "log.txt"

    #  File handling with 'with' and 'try'
    try:
        # We use 'with' so the file closes automatically no matter what
        with open(filename, "a") as log:
            try:
                # Try block: The risky code
                val1 = int(input("Enter numerator: "))
                val2 = int(input("Enter denominator: "))

                #  Raising your own errors
                if val1 < 0 or val2 < 0:
                    raise NegativeNumberError("This app only likes positive numbers!")

                result = val1 / val2

            #  Catching multiple specific exceptions
            except ValueError:
                error_msg = "Error: Please enter actual numbers, not letters.\n"
                print(error_msg)
                log.write(error_msg)
            
            except ZeroDivisionError:
                error_msg = "Error: You cannot divide by zero!\n"
                print(error_msg)
                log.write(error_msg)

            except NegativeNumberError as e:
                print(f"Custom Error: {e}")
                log.write(f"Negative Input Error: {e}\n")

            #  Else: Runs ONLY if no error happened
            else:
                success_msg = f"Success! Result: {result}\n"
                print(success_msg)
                log.write(success_msg)

            # Finally: Runs every single time
            finally:
                print("Calculation attempt finished.")

    except IOError:
        print("Fatal Error: Could not write to log file!")

# --- Execution ---
if __name__ == "__main__":
    secure_divider()

"""
SAMPLE OUTPUT (Scenario: User enters 10 and 0):
--- Welcome to the Secure Divider ---
Enter numerator: 10
Enter denominator: 0
Error: You cannot divide by zero!
Calculation attempt finished.

SAMPLE OUTPUT (Scenario: User enters 10 and 2):
--- Welcome to the Secure Divider ---
Enter numerator: 10
Enter denominator: 2
Success! Result: 5.0
Calculation attempt finished.
"""