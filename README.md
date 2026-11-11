# lab2_Genereuse3: ALU Transcript Generator

A Python program and a Bash script for the Individual Coding Lab (Lab 2).

- `grade-evaluator.py` reads a CSV of course grades, validates it, calculates the final grade and GPA, decides PASSED or FAILED, and lists the assignments eligible for resubmission.
- `organizer.sh` archives the grades file with a timestamp, creates a fresh empty `grades.csv`, and logs what it did.

## Files

| File | Purpose |
|---|---|
| `grade-evaluator.py` | The grade evaluator (Python) |
| `grades.csv` | The sample course grades |
| `organizer.sh` | The archiving script (Bash) |
| `README.md` | This file |
| `.gitignore` | Keeps Python cache files and test CSV files out of the repository |

## Requirements

Python 3 and Bash. Only Python standard-library modules are used (`csv`, `sys`, `os`); there are no external libraries.

## Run the evaluator

```
python3 grade-evaluator.py
```

The program asks: `Enter the name of the CSV file to process (e.g., grades.csv):`. Type the file name and press Enter.

The CSV file needs this header and one row per assignment:

```
assignment,group,score,weight
Quiz,Formative,85,20
```

`group` is Formative or Summative (any capitalisation is accepted), `score` is a number from 0 to 100, and `weight` is a number.

Output for the sample `grades.csv`:

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

## How it works

1. **Load the file.** Each row becomes a record with the assignment name, group, score and weight. Problems in the file are reported before any calculation .
2. **Validate the scores.** Every score must be between 0 and 100 (0 and 100 are allowed). Each bad score is reported by assignment name.
3. **Validate the weights.** All weights must add up to exactly 100, the Formative weights to 60, and the Summative weights to 40. Each failed check is reported with the real total.
4. **Final grade and GPA.** Each assignment contributes `score x weight / 100` points. The Final Grade is the sum of these points (out of 100) and `GPA = (Final Grade / 100) x 5.0`.
5. **Pass or fail.** A category percentage is the points earned in that category divided by the weight available in that category, times 100. The student passes only with at least 50% in **both** Formative and Summative. Exactly 50% passes.
6. **Resubmission.** A failed Formative assignment has a score below 50 (exactly 50 is not a fail). Among the failed Formative assignments, the ones with the highest weight are eligible. If several share that highest weight, all of them are listed.

### Worked example (sample `grades.csv`)

| Assignment | Group | Score | Weight | Points |
|---|---|---|---|---|
| Quiz | Formative | 85 | 20 | 17 |
| Group Exercise | Formative | 40 | 20 | 8 |
| Functions and Debugging Lab | Formative | 45 | 20 | 9 |
| Midterm Project - Simple Calculator | Summative | 70 | 20 | 14 |
| Final Project - Text-Based Game | Summative | 60 | 20 | 12 |

- Final Grade: 17 + 8 + 9 + 14 + 12 = 60, so GPA = 60 / 100 x 5.0 = 3.00
- Formative: 34 / 60 = 56.67%. Summative: 26 / 40 = 65.00%. Both are at least 50%, so the status is PASSED.
- Failed Formative assignments: Group Exercise (40) and Functions and Debugging Lab (45). Both have weight 20, so both are eligible for resubmission.

### Design decisions

- Resubmission is shown whether the student passed or failed overall, because the rule is about failed Formative assignments, not about the final status.
- Group names are accepted in any capitalisation (`formative` is read as Formative).
- Completely blank rows are skipped with a note. Rows with an empty score or weight are rejected.

## Edge cases and validation

| Situation | What the program does |
|---|---|
| File does not exist | Prints that the file was not found and stops |
| File is empty | Prints that the file is empty |
| Header but no rows | Prints that there are no assignment rows |
| A column is missing | Lists the missing columns and the expected header |
| Score or weight is text or empty | Reports the row number, the assignment and the values found |
| Group is not Formative or Summative | Reports the row number and the assignment |
| Completely blank row | Skips it and prints how many were skipped |
| Score outside 0 to 100 | Reports each assignment with a bad score |
| Weights do not add up | Reports the real total, Formative total or Summative total |

Every case ends with a clear message and no Python error trace.

## Run the organizer

```
bash organizer.sh
```

Run it in the folder that contains `grades.csv`. It does the following:

1. Stops with an error and exit code 1 if `grades.csv` does not exist.
2. Creates the `archive` directory if it is missing.
3. Moves `grades.csv` into `archive/` and renames it with a timestamp, for example `archive/grades_20251105-170000.csv`.
4. Immediately creates a new, empty `grades.csv`.
5. Appends one line to `organizer.log` with the timestamp, the original file name and the archived file name. The log keeps the entries from every run.

Example log line:

```
20251105-170000 | original: grades.csv | archived: archive/grades_20251105-170000.csv
```

Warning: the script empties `grades.csv`. To try it, run it in a copy of the folder, or copy the archived file back afterwards.

## Testing

Create the test files from the sample `grades.csv`:

```
sed 's/,85,/,105,/; s/,40,/,-5,/' grades.csv > test_bad_score.csv
sed '2s/,20$/,25/' grades.csv > test_bad_weight.csv
sed '5s/Summative/Formative/' grades.csv > test_bad_split.csv
sed '5s/,70,/,30,/; 6s/,60,/,30,/' grades.csv > test_fail.csv
sed '3s/,40,/,90,/; 4s/,45,/,90,/' grades.csv > test_no_resubmit.csv
printf '' > test_empty.csv
printf 'assignment,group,score,weight\n' > test_header_only.csv
printf 'assignment,group,score\nQuiz,Formative,85\n' > test_missing_column.csv
sed '2s/,85,/,abc,/' grades.csv > test_text_score.csv
sed '2s/,85,/,,/' grades.csv > test_empty_score.csv
sed '2a ,,,' grades.csv > test_blank_row.csv
sed '2s/Formative/Homework/' grades.csv > test_bad_group.csv
printf 'assignment,group,score,weight\nQuiz,Formative,50,20\nGroup Exercise,Formative,50,20\nFunctions Lab,Formative,50,20\nMidterm,Summative,50,20\nFinal,Summative,50,20\n' > test_all_50.csv
printf 'assignment,group,score,weight\nQuiz,Formative,49,20\nGroup Exercise,Formative,49,20\nFunctions Lab,Formative,49,20\nMidterm,Summative,100,20\nFinal,Summative,100,20\n' > test_form_49.csv
printf 'assignment,group,score,weight\nQuiz,Formative,30,20\nGroup Exercise,Formative,70,20\nFunctions Lab,Formative,50,20\nMidterm,Summative,70,20\nFinal,Summative,60,20\n' > test_pass_but_resub.csv
```

Run all of them in one go (the file name is passed to the program's prompt):

```
for f in test_bad_score test_bad_weight test_bad_split test_fail test_no_resubmit test_empty test_header_only test_missing_column test_text_score test_empty_score test_blank_row test_bad_group test_all_50 test_form_49 test_pass_but_resub; do echo "=== $f ==="; echo $f.csv | python3 grade-evaluator.py; done
```

Expected results:

| Test file | Expected result |
|---|---|
| `grades.csv` | 60.00, GPA 3.00, Formative 56.67%, Summative 65.00%, PASSED, two resubmissions |
| `test_bad_score.csv` | Errors for Quiz (105.0) and Group Exercise (-5.0); nothing is calculated |
| `test_bad_weight.csv` | Errors: total weight 105.0 and Formative weights 65.0 |
| `test_bad_split.csv` | Errors: Formative 80.0 and Summative 20.0 (the total is still 100) |
| `test_fail.csv` | 46.00, GPA 2.30, Summative 30.00%, FAILED, two resubmissions |
| `test_no_resubmit.csv` | 79.00, GPA 3.95, PASSED, no resubmission |
| `test_empty.csv` | The file is empty |
| `test_header_only.csv` | No assignment rows |
| `test_missing_column.csv` | Missing column: weight |
| `test_text_score.csv` | Row 2 ('Quiz'): found score='abc' |
| `test_empty_score.csv` | Row 2 ('Quiz'): found score='' |
| `test_blank_row.csv` | 1 empty row skipped, then the normal sample result |
| `test_bad_group.csv` | Row 2 ('Quiz'): group must be Formative or Summative |
| `test_all_50.csv` | 50.00, GPA 2.50, exactly 50% in both categories: PASSED, no resubmission |
| `test_form_49.csv` | Formative 49.00%: FAILED, three tied resubmissions |
| `test_pass_but_resub.csv` | 56.00, GPA 2.80, PASSED, but Quiz (30) is still eligible |

For `organizer.sh`, run it in a scratch copy: the first run creates `archive/` and leaves a 0-byte `grades.csv`; a second run adds a second line to `organizer.log`; running it with no `grades.csv` prints an error and returns exit code 1.

## Known limitations

- Negative weights are not rejected on their own; only the totals are checked.
- Duplicate assignment names are not detected.
- Two runs of `organizer.sh` within the same second would use the same archive file name.
- Scores and weights may be decimals, and percentages are calculated with floating-point numbers.
