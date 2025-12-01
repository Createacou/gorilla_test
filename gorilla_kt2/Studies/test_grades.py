import pytest
from grades import read_grades_from_csv, calculate_average, grade_from_average

@pytest.mark.parametrize("row", list(read_grades_from_csv("grades.csv")))
def test_grades(row):
    name = f"{row['First name']} {row['Last name']}"
    expected_grade = row["Grade"].strip()

    try:
        avg = calculate_average(row)
        computed_grade = grade_from_average(avg)
    except ValueError as e:
    
        assert False, f"Ошибка в данных для {name}: {e}"
        
    assert computed_grade == expected_grade, f"Несоответствие для {name}: вычислено {computed_grade}, ожидалось {expected_grade}"