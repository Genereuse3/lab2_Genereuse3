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

def calculate_grade(data):
    total_grade = 0
    for row in data:
        total_grade = total_grade + row["score"] * row["weight"] / 100
    gpa = (total_grade / 100) * 5.0
    return total_grade, gpa

def get_category_percentages(data):
    formative_earned = 0
    formative_possible = 0
    summative_earned = 0
    summative_possible = 0
    for row in data:
        points = row["score"] * row["weight"] / 100
        if row["group"] == "Formative":
            formative_earned = formative_earned + points
            formative_possible = formative_possible + row["weight"]
        elif row["group"] == "Summative":
            summative_earned = summative_earned + points
            summative_possible = summative_possible + row["weight"]
    formative_pct = formative_earned / formative_possible * 100
    summative_pct = summative_earned / summative_possible * 100
    return formative_pct, summative_pct


def find_resubmissions(data):
    failed = []
    for row in data:
        if row["group"] == "Formative" and row["score"] < 50:
            failed.append(row)
    if len(failed) == 0:
        return []
    highest = 0
    for row in failed:
        if row["weight"] > highest:
            highest = row["weight"]
    eligible = []
    for row in failed:
        if row["weight"] == highest:
            eligible.append(row)
    return eligible

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
    
    total_grade, gpa = calculate_grade(data)
    formative_pct, summative_pct = get_category_percentages(data)
    print(f"Final Grade: {total_grade:.2f} / 100")
    print(f"GPA: {gpa:.2f}")
    print(f"Formative: {formative_pct:.2f}% Summative: {summative_pct:.2f}%")
    if formative_pct >= 50 and summative_pct >= 50:
        print("Status: PASSED")
    else:
        print("Status: FAILED")
    eligible = find_resubmissions(data)
    if len(eligible) == 0:
        print("Resubmission: none(no failed Formative assignments)")
    else:
        print("Eligible for resubmission (highest-weight failed Formative):")
        for row in eligible:
            print(f"  - {row['assignment']} (score {row['score']:.0f}, weight {row['weight']:.0f})")

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
