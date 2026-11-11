1 lab2_ALU Transcript Generator

This is my Python program and a Bash script for lab 2. It checks grades from a CSV file and calculates the final grade



2 Files table

| File | Purpose |
|---|---|
| `grade-evaluator.py` | The main python file |
| `grades.csv` | The grades file that was used to test |
| `organizer.sh` | The bash script that archives grades.csv |
| `README.md` | This file |


3 Requirements

I only used Python's built in modules, i did not use any external library

4 Run the evaluator

to run it , it is just typing python3 grade-evaluator.py then type the file name when it asks you like grades.csv

5 Output for the sample `grades.csv`:

```
--- Processing Grades ---
Final Grade: 60.00 / 100
GPA: 3.00
Formative: 56.67% Summative: 65.00%
Status: PASSED
Eligible for resubmission (highest-weight failed Formative):
  - Group Exercise (score 40, weight 20)
  - Functions and Debugging Lab (score 45, weight 20)
```
this is what i got when i ran it


6 How it works

1.First the program reads the CSV file
2.Then it checks if any score is less than 0 or more than 100. If there is a bad score, it shows the assignment name and stops
3.After that it checks the weight. All weights together must be 100. where Formative must be 60 and Summative must be 40.
4. For the final grade , I did score *weight/100 for each assignment and added them all and then for GPA= final grade/ 100 * 5
5.To pass, you need at least 50% in BOTH Formative and Summative. Exactly 50% is a pass
6. For resubmission, I only looked at failed Formative assignments (score < 50). I found the one with the highest weight. If two have the same weight, I show both. This is shown even if the student passed overall, because it is only about Formative
7. Group names are accepted in any capitalisation formative is read as Formative.
8. Completely blank rows are skipped with a note. Rows with an empty score or weight are rejected.

7 Example with a sample file

| Assignment | Group | Score | Weight | Points |
|---|---|---|---|---|
| Quiz | Formative | 85 | 20 | 17 |
| Group Exercise | Formative | 40 | 20 | 8 |
| Functions and Debugging Lab | Formative | 45 | 20 | 9 |
| Midterm Project - Simple Calculator | Summative | 70 | 20 | 14 |
| Final Project - Text-Based Game | Summative | 60 | 20 | 12 |

- Final Grade: 17 + 8 + 9 + 14 + 12 = 60, so GPA = 60 / 100 * 5.0 = 3.00
- Formative: 34 / 60 = 56.67%. Summative: 26 / 40 = 65.00%. Both are at least 50%, so the status is PASSED.
- Failed Formative assignments: Group Exercise (40) and Functions and Debugging Lab (45). Both have weight 20, so both are eligible for resubmission.

8 Edge cases table


| Situation | What the program does |
|---|---|
| File does not exist | Prints that the file was not found and stops |
| File is empty | Prints that the file is empty |
| Score outside 0 to 100 | Reports each assignment with a bad score |
| Weights do not add up to 100| Reports the real total, Formative total or Summative total |

9 Run the organizer

To run it, type bash organizer.sh. It will create a folder called archive if it doesn't exist, move grades.csv there with a timestamp like grades_20251105-170000.csv, make a new empty grades.csv, and write everything in organizer.log.



Example log line:

```
20251105-170000 | original: grades.csv | archived: archive/grades_20251105-170000.csv
```

Warning: the script empties `grades.csv`. To try it, run it in a copy of the folder, or copy the archived file back afterwards.

10 Testing

I tested it by making small copies of grades.csv and changing one thing each time, for example changing a score to 105 to check if it gives an error, and changing the weights so they don't add up to 100


Expected results:

| Test file | Expected result |
|---|---|
| `test_bad_score.csv` | Errors for Quiz (105.0) and Group Exercise (-5.0); nothing is calculated |
| `test_bad_weight.csv` | Errors: total weight 105.0 and Formative weights 65.0 |
| `test_bad_split.csv` | Errors: Formative 80.0 and Summative 20.0 (the total is still 100) |
| `test_fail.csv` | 45.00, GPA 2.25, Formative 55.00%, Summative 30.00%, FAILED, two resubmissions |
| `test_no_resubmit.csv` | 79.00, GPA 3.95, PASSED, no resubmission |
| `test_empty.csv` | The file is empty |
| `test_bad_group.csv` | Row 2 ('Quiz'): group must be Formative or Summative |
| `test_all_50.csv` | 50.00, GPA 2.50, exactly 50% in both categories: PASSED, no resubmission |

For organizer.sh, run it in a copy of the folder: the first run creates archive/ and leaves an empty grades.csv; a second run adds a second line to organizer.log; running it with no grades.csv prints an error


