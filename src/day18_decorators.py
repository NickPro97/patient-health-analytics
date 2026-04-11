"""
Day 18: Decorators
==================
Nikhil's AI/ML Journey — April 8, 2026

Concept: A decorator WRAPS a function to add behavior
without changing the original function.

Pattern:
    def decorator(func):
        def wrapper(*args, **kwargs):
            # do something before
            result = func(*args, **kwargs)
            # do something after
            return result
        return wrapper
"""

# ============================================
# EXAMPLE 1: Simple decorator (no arguments)
# ============================================
def shout(func):
    """Makes any function's string result UPPERCASE"""
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

@shout
def greet():
    return "hello, welcome to healthcare ai"

print("Example 1:", greet())
# Without @shout, this would print: hello, welcome to healthcare ai
# With @shout, it prints: HELLO, WELCOME TO HEALTHCARE AI


# ============================================
# EXAMPLE 2: Decorator WITH function arguments
# ============================================
# Problem: wrapper() above takes NO arguments.
# If the wrapped function needs arguments, wrapper must accept them too.
# Solution: *args, **kwargs — accepts ANY arguments and passes them through.

import time

def timer(func):
    """Measures how long a function takes to run"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)  # pass all args through
        end = time.time()
        print(f"  ⏱ {func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_add(a, b):
    """Adds two numbers slowly (simulating data processing)"""
    time.sleep(0.5)  # simulate slow work
    return a + b

print("\nExample 2:")
answer = slow_add(10, 20)
print(f"  Result: {answer}")


# ============================================
# EXAMPLE 3: Logger decorator (YOUR P1 NEED!)
# ============================================
# In healthcare, you MUST log who accessed what data and when.
# A decorator makes this automatic — every function call gets logged.

from datetime import datetime

def log_access(func):
    """Logs every function call with timestamp — HIPAA audit trail"""
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  📋 LOG: {func.__name__} called at {timestamp}")
        print(f"       Args: {args}, Kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"       ✅ Completed successfully")
        return result
    return wrapper

@log_access
def get_patient_vitals(patient_id: int):
    """Simulates fetching patient vitals"""
    # In real P1, this would query your MIMIC-III data
    fake_vitals = {"heart_rate": 82, "bp_systolic": 120, "spo2": 97}
    return fake_vitals

print("\nExample 3:")
vitals = get_patient_vitals(40124)
print(f"  Vitals: {vitals}")


# ============================================
# EXAMPLE 4: Stacking decorators
# ============================================
# You can use MULTIPLE decorators on one function!
# They apply bottom-up: closest to function runs first.

@timer
@log_access
def process_patient_data(patient_id: int, data_type: str = "vitals"):
    """Simulates processing patient data — logged AND timed"""
    time.sleep(0.3)
    return f"Processed {data_type} for patient {patient_id}"

print("\nExample 4 (stacked decorators):")
result = process_patient_data(40124, data_type="vitals")
print(f"  Result: {result}")


# ============================================
# EXERCISE 1: Build a validate_patient_id decorator
# ============================================
# Requirements:
# - Check that patient_id (first argument) is a positive integer
# - If not valid, print an error and return None instead of calling the function
# - If valid, call the function normally
#
# Hint: args[0] gives you the first argument

def validate_patient_id(func):
    def wrapper(*args, **kwargs):
        # YOUR CODE HERE
        # 1. Get patient_id from args[0]
        # 2. Check: is it an int? is it > 0?
        # 3. If not valid: print error, return None
        # 4. If valid: return func(*args, **kwargs)
        patient_id = args[0]

        if not isinstance(patient_id, int) or patient_id <= 0:
            print(f"Error patient id : {patient_id} <= 0")
            return None
        return func(*args, **kwargs)
        pass
    return wrapper

# Uncomment when ready:
@validate_patient_id
def lookup_patient(patient_id: int):
    return f"Found patient {patient_id}"

print("\nExercise 1:")
print(lookup_patient(40124))    # Should work
print(lookup_patient(-5))       # Should print error, return None
print(lookup_patient("abc"))    # Should print error, return None


# ============================================
# EXERCISE 2: Build a retry decorator
# ============================================
# In production, API calls fail sometimes. A retry decorator
# automatically tries again if a function raises an exception.
#
# Requirements:
# - Try calling the function
# - If it raises an exception, print a warning and try again
# - Try up to 3 times total
# - If all 3 fail, print final error and return None
#
# Hint: use a for loop with try/except inside wrapper

def retry(func):
    def wrapper(*args, **kwargs):
        # for attempt in range(3):
        #     try: ...
        #     except Exception as e: ...
        for attempt in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"attempt {attempt + 1} error : {e}")
        return None
    return wrapper

import random
@retry
def flaky_api_call(patient_id):
    """Simulates an unreliable API — fails 70% of the time"""
    if random.random() < 0.7:
        raise ConnectionError("API timeout!")
    return f"Got data for patient {patient_id}"

print("\nExercise 2:")
print(flaky_api_call(40124))


# ============================================
# EXERCISE 3 (CHALLENGE): Build a role_required decorator
# ============================================
# Healthcare apps need access control.
# Only certain roles (doctor, nurse, admin) can access patient data.
#
# This is a DECORATOR WITH ARGUMENTS — a decorator factory!
# Pattern:
#   def role_required(allowed_roles):    # outer: takes decorator args
#       def decorator(func):             # middle: takes function
#           def wrapper(*args, **kwargs): # inner: takes function args
#               ...
#           return wrapper
#       return decorator
#
# Requirements:
# - role_required takes a list of allowed roles
# - wrapper checks if current_user_role (global variable) is in allowed_roles
# - If allowed: call function normally
# - If denied: print "ACCESS DENIED" and return None

current_user_role = "nurse"  # Change this to test different roles

def role_required(allowed_roles):
    # YOUR CODE HERE — three levels of nesting!
    def decorator(func):
        def wrapper(*args, **kwargs):
            if current_user_role in allowed_roles:
                return func(*args, **kwargs)
            else:
                print("ACCESS DENIED")
                return None
        return wrapper
    return decorator

# Uncomment when ready:
@role_required(["doctor", "admin"])
def view_full_record(patient_id):
    return f"Full medical record for patient {patient_id}"

@role_required(["doctor", "nurse", "admin"])
def view_vitals(patient_id):
    return f"Vitals for patient {patient_id}"

print("\nExercise 3:")
print(f"Current role: {current_user_role}")
print(view_vitals(40124))       # nurse CAN see vitals
print(view_full_record(40124))  # nurse CANNOT see full record
