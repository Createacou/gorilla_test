import csv

def clean_headers(reader):
    reader.fieldnames = [name.strip() for name in reader.fieldnames]
    return reader

def read_grades_from_csv(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        reader = clean_headers(reader)  
        for row in reader:
            yield row

def calculate_average(row):
    tests = ["Test1", "Test2", "Test3", "Test4", "Final"]
    scores = []
    for t in tests:
        val = float(row[t])
        if val < 0:
            raise ValueError(f"Negative score found: {val}")
        scores.append(val)
    return sum(scores) / len(scores)

def grade_from_average(avg):
    if avg >= 97:
        return "A+"
    elif avg >= 93:
        return "A"
    elif avg >= 90:
        return "A-"
    elif avg >= 87:
        return "B+"
    elif avg >= 83:
        return "B"
    elif avg >= 80:
        return "B-"
    elif avg >= 77:
        return "C+"
    elif avg >= 73:
        return "C"
    elif avg >= 70:
        return "C-"
    elif avg >= 67:
        return "D+"
    elif avg >= 63:
        return "D"
    elif avg >= 60:
        return "D-"
    else:
        return "F"