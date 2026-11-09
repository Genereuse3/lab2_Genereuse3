import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def validate_scores(data):
    all_ok = True
    for row in data:
        if row["score"] < 0 or row["score"] > 100:
            print(f"Error: '{row['assignment']}' has a score of {row['score']}, which must be between 0 and 100.")
            all_ok = False
    return all_ok




def validate_weights(data):
    total = 0
    formative = 0
    summative = 0
    for row in data:
        total = total + row["weight"]
        if row["group"] == "Formative":
            formative = formative + row["weight"]
        elif row["group"] == "Summative":
            summative = summative + row["weight"]
    all_ok = True
    if total != 100:
        print(f"Error: total weight is {total}, but it must be 100.")
        all_ok = False
    if formative != 60:
        print(f"Error: Formative weights add up to {formative}, but they must be 60.")
        all_ok = False
    if summative != 40:
        print(f"Error: Summative weights add up to {summative}, but they must be 40.")
        all_ok = False
    return all_ok

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
    if not validate_scores(data):
        return
    if not validate_weights(data):
        return
    
    # TODO: a) Check if all scores are percentage based (0-100)
    # TODO: b) Validate total weights (Total=100, Summative=40, Formative=60)
    # TODO: c) Calculate the Final Grade and GPA
    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    # TODO: e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for resubmission.
    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options
    
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
