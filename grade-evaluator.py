import csv
import sys
import os

# Ask for file name and read it
filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

if not os.path.exists(filename):
    print(f"Error: The file '{filename}' was not found.")
    sys.exit(1)

if not os.path.isfile(filename):
    print(f"Error: '{filename}' is not a file.")
    sys.exit(1)

assignments = []

with open(filename, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    if reader.fieldnames is None:
        print(f"Error: The file '{filename}' is empty.")
        sys.exit(1)

    required = ["assignment", "group", "score", "weight"]
    missing = []
    for column in required:
        if column not in reader.fieldnames:
            missing.append(column)
    if len(missing) > 0:
        print(f"Error: The file is missing column(s): {', '.join(missing)}.")
        print("Expected header: assignment,group,score,weight")
        sys.exit(1)

    skipped = 0
    line_number = 1

    for row in reader:
        line_number = line_number + 1
        name = (row["assignment"] or "").strip()
        group = (row["group"] or "").strip().capitalize()
        score_text = (row["score"] or "").strip()
        weight_text = (row["weight"] or "").strip()

        # skip completely empty row
        if name == "" and group == "" and score_text == "" and weight_text == "":
            skipped = skipped + 1
            continue

        # if score or weight is empty, stop
        if score_text == "" or weight_text == "":
            print(f"Error: Row {line_number} ('{name}'): score or weight is empty.")
            sys.exit(1)

        if group != "Formative" and group != "Summative":
            print(f"Error: Row {line_number} ('{name}'): group must be Formative or Summative.")
            sys.exit(1)

        # turn text into numbers
        try:
            score = float(score_text)
            weight = float(weight_text)
        except ValueError:
            print(f"Error: Row {line_number} ('{name}'): score and weight must be numbers.")
            sys.exit(1)

        assignments.append({"assignment": name, "group": group, "score": score, "weight": weight})

    if skipped > 0:
        print(f"Note: {skipped} empty row(s) were skipped.")

if len(assignments) == 0:
    print("Error: the file has a header but no assignment rows.")
    sys.exit(1)

print("\n--- Processing Grades ---")

# 1. Check scores are 0 to 100
for row in assignments:
    if row["score"] < 0 or row["score"] > 100:
        print(f"Error: '{row['assignment']}' has a score of {row['score']}, which must be between 0 and 100.")
        sys.exit(1)

# 2. Check weights
total_weight = 0
formative_weight = 0
summative_weight = 0
for row in assignments:
    total_weight = total_weight + row["weight"]
    if row["group"] == "Formative":
        formative_weight = formative_weight + row["weight"]
    else:
        summative_weight = summative_weight + row["weight"]

if total_weight != 100:
    print(f"Error: total weight is {total_weight}, but it must be 100.")
    sys.exit(1)
if formative_weight != 60:
    print(f"Error: Formative weights add up to {formative_weight}, but they must be 60.")
    sys.exit(1)
if summative_weight != 40:
    print(f"Error: Summative weights add up to {summative_weight}, but they must be 40.")
    sys.exit(1)

# 3. Calculate final grade and GPA
# points for one assignment = score * weight / 100
total_grade = 0
formative_earned = 0
summative_earned = 0

for row in assignments:
    points = row["score"] * row["weight"] / 100
    total_grade = total_grade + points
    if row["group"] == "Formative":
        formative_earned = formative_earned + points
    else:
        summative_earned = summative_earned + points

gpa = (total_grade / 100) * 5.0

# formative % = what we got / what was possible. Possible is 60.
formative_pct = formative_earned / 60 * 100
summative_pct = summative_earned / 40 * 100

print(f"Final Grade: {total_grade:.2f} / 100")
print(f"GPA: {gpa:.2f}")
print(f"Formative: {formative_pct:.2f}% Summative: {summative_pct:.2f}%")

if formative_pct >= 50 and summative_pct >= 50:
    print("Status: PASSED")
else:
    print("Status: FAILED")

# 4. Find resubmissions - only failed Formative
failed = []
for row in assignments:
    if row["group"] == "Formative" and row["score"] < 50:
        failed.append(row)

if len(failed) == 0:
    print("Resubmission: none (no failed Formative assignments)")
else:
    # find the biggest weight among failed ones
    highest = 0
    for row in failed:
        if row["weight"] > highest:
            highest = row["weight"]
    print("Eligible for resubmission (highest-weight failed Formative):")
    for row in failed:
        if row["weight"] == highest:
            print(f"  - {row['assignment']} (score {row['score']:.0f}, weight {row['weight']:.0f})")
