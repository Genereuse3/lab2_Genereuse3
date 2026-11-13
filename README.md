# lab2_ALU Transcript Generator

This is my Python program and a Bash script for lab 2. It checks grades from a CSV file and calculates the final grade



## Files table

| File | Purpose |
|---|---|
| `grade-evaluator.py` | The main python file |
| `grades.csv` | The grades file that was used to test |
| `organizer.sh` | The bash script that archives grades.csv |
| `README.md` | This file |


## Requirements

I only used Python's built in modules, i did not use any external library

## Run the evaluator
to run it , it is just typing python3 grade-evaluator.py then type the file name when it asks you like grades.csv

## Output for the sample `grades.csv`:

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

## How it works

1. First the program reads the CSV file
2. Then it checks if any score is less than 0 or more than 100. If there is a bad score, it shows the assignment name and stops
3. After that it checks the weight. All weights together must be 100. where Formative must be 60 and Summative must be 40.
4. For the final grade , I did score *weight/100 for each assignment and added them all and then for GPA= final grade/ 100 * 5
5. To pass, you need at least 50% in BOTH Formative and Summative. Exactly 50% is a pass
6. For resubmission, I only looked at failed Formative assignments (score < 50). I found the one with the highest weight. If two have the same weight, I show both. This is shown even if the student passed overall, because it is only about Formative
7. Group names are accepted in any capitalisation formative is read as Formative.
8. Completely blank rows are skipped with a note. Rows with an empty score or weight are rejected.

## Example with a sample file

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

## Edge cases table

| Situation | What the program does |
|---|---|
| File does not exist | Prints that the file was not found and stops |
| File is empty | Prints that the file is empty |
| Score outside 0 to 100 | Reports the first assignment with a bad score and stops |
| Weights do not add up to 100| Reports the first weight check that fails (total, Formative or Summative) and stops |

## Run the organizer
To run it, type bash organizer.sh. It will create a folder called archive if it doesn't exist, move grades.csv there with a timestamp like grades_20251105-170000.csv, make a new empty grades.csv, and write everything in organizer.log.



Example log line:

```
20251105-170000 | original: grades.csv | archived: archive/grades_20251105-170000.csv
```

Warning: the script empties `grades.csv`. To try it, run it in a copy of the folder, or copy the archived file back afterwards.

## Testing
I tested it by making small copies of grades.csv and changing one thing each time, for example changing a score to 105 to check if it gives an error, and changing the weights so they don't add up to 100


Expected results:

| Test file | Expected result |
|---|---|
| `test_bad_score.csv` | Error for Quiz (105.0); the program stops |
| `test_bad_weight.csv` | Error: total weight is 105.0; the program stops |
| `test_bad_split.csv` | Error: Formative weights add up to 80.0 (the total is still 100); the program stops |
| `test_fail.csv` | 45.00, GPA 2.25, Formative 55.00%, Summative 30.00%, FAILED, two resubmissions |
| `test_no_resubmit.csv` | 79.00, GPA 3.95, PASSED, no resubmission |
| `test_empty.csv` | The file is empty |
| `test_header_only.csv` | No assignment rows |
| `test_missing_column.csv` | Missing column: weight |
| `test_text_score.csv` | Row 2 ('Quiz'): found score='abc' |
| `test_empty_score.csv` | Row 2 ('Quiz'): found score='' |
| `test_blank_row.csv` | 1 empty row skipped, then the normal sample result |
| `test_bad_group.csv` | Row 2 ('Quiz'): group must be Formative or Summative |
| `test_all_50.csv` | 50.00, GPA 2.50, exactly 50% in both categories: PASSED, no resubmission |

For organizer.sh, run it in a copy of the folder: the first run creates archive/ and leaves an empty grades.csv; a second run adds a second line to organizer.log; running it with no grades.csv prints an error



## Create the test files

```
sed 's/,85,/,105,/; s/,40,/,-5,/' grades.csv > test_bad_score.csv
sed '2s/,20$/,25/' grades.csv > test_bad_weight.csv
sed '5s/Summative/Formative/' grades.csv > test_bad_split.csv
sed '5s/,70,/,30,/; 6s/,60,/,30,/' grades.csv > test_fail.csv
sed '3s/,40,/,90,/; 4s/,45,/,90,/' grades.csv > test_no_resubmit.csv
printf '' > test_empty.csv
sed '2s/Formative/Homework/' grades.csv > test_bad_group.csv
printf 'assignment,group,score\nQuiz,Formative,85\n' > test_missing_column.csv
printf 'assignment,group,score,weight\nQuiz,Formative,50,20\nGroup Exercise,Formative,50,20\nFunctions Lab,Formative,50,20\nMidterm,Summative,50,20\nFinal,Summative,50,20\n' > test_all_50.csv
```

A file with a missing column prints which columns are missing.
