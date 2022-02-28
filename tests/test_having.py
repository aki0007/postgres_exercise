import pytest
import datetime


@pytest.mark.parametrize("database", ["Employees"])
@pytest.mark.having
def test_show_employees_hired_after_1991_having_more_then_two_titles(cursor_dict, database):
    """
    Show me all the employees, hired after 1991, that have had more than 2 titles
    """
    query = """
    SELECT e.emp_no, count(t.title)
    FROM employees AS e
    JOIN titles AS t USING(emp_no)
    WHERE EXTRACT(year FROM e.hire_date) > 1991
    GROUP BY e.emp_no
    HAVING count(t.title) >= 2
    ORDER BY e.emp_no;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)
    # Extract and print data from query
    rows = cursor.fetchall()
    print("\nemp_no | amount of titles")
    for r in rows:
        print(f"{r[0]} | {r[1]}")

    # Validate data in first row and all data length
    assert rows[0][0] == 10012
    assert rows[0][1] == 2
    assert len(rows) == 25086


@pytest.mark.parametrize("database", ["Employees"])
@pytest.mark.having
def test_show_employees_from_development_with_more_then_fifteen_raises(cursor_dict, database):
    """
    Show me all the employees that have had more than 15 salary changes that work in the department development
    """
    query = """
    SELECT e.emp_no, count(s.salary) 
    FROM employees AS e
    JOIN dept_emp as d USING(emp_no)
    join salaries as s USING(emp_no)
    WHERE d.dept_no = 'd005'
    GROUP BY e.emp_no
    HAVING count(s.salary) > 15
    ORDER BY e.emp_no;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)
    # Extract and print data from query
    rows = cursor.fetchall()
    print("\nemp_no | amount of raises")
    for r in rows:
        print(f"{r[0]} | {r[1]}")

    # Validate data in first row and all data length
    assert rows[0][0] == 10001
    assert rows[0][1] == 17
    assert len(rows) == 11493


@pytest.mark.parametrize("database", ["Employees"])
@pytest.mark.having
def test_show_employees_that_worked_for_multiple_departments(cursor_dict, database):
    """
    Show me all the employees that have worked for multiple departments
    """
    query = """
    SELECT e.emp_no, count(d.dept_no)
    FROM employees as e
    JOIN dept_emp as d USING(emp_no)
    GROUP BY e.emp_no
    HAVING count(d.dept_no) > 1
    ORDER BY e.emp_no;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)
    # Extract and print data from query
    rows = cursor.fetchall()
    print("\nemp_no | amount of departments")
    for r in rows:
        print(f"{r[0]} | {r[1]}")

    # Validate data in first row and all data length
    assert rows[0][0] == 10010
    assert rows[0][1] == 2
    assert len(rows) == 31579
