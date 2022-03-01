import pytest
import datetime


@pytest.mark.parametrize("database", ["Employees"])
@pytest.mark.view
def test_view_1985_1986(cursor_dict, database):
    """
    Create a view "85-86" that shows all the employees, hired between 1985 and 1986
    """
    view = """
    CREATE OR REPLACE VIEW employees_hired_between_1985_1986 AS
    SELECT * from employees 
    WHERE EXTRACT(YEAR FROM hire_date) BETWEEN 1985 and 1986
    ORDER BY emp_no;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(view)

    # Execute view and check if all info are returned
    cursor.execute("SELECT * FROM employees_hired_between_1985_1986 ORDER BY emp_no")

    # Extract and print data from query
    rows = cursor.fetchall()

    print("\nemp_no | birth_date | first_name | last_name | gender | hire_date |")
    for r in rows:
        print(f"{r[0]} | {r[1]}| {r[2]} | {r[3]} | {r[4]} | {r[5]}")

    # Validate data in first row and all data length
    assert rows[0][0] == 10001
    assert rows[0][1] == datetime.date(1953, 9, 2)
    assert rows[0][2] == "Georgi"
    assert rows[0][3] == "Facello"
    assert rows[0][4] == "M"
    assert rows[0][5] == datetime.date(1986, 6, 26)

    assert len(rows) == 71466


@pytest.mark.parametrize("database", ["Employees"])
@pytest.mark.view
def test_view_bigbucks(cursor_dict, database):
    """
    Create a view "90-95" that:
    Shows me all the employees, hired between 1990 and 1991

    LIST INDEX OUT OF RANGE ERROR
    """
    view = """
    CREATE OR REPLACE VIEW bigbucks AS 
    SELECT distinct on (e.emp_no)
    e.emp_no, s.salary FROM Employees as e
    JOIN salaries as s USING(emp_no)
    WHERE s.salary > 120000
    ORDER BY e.emp_no
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(view)

    # Execute view and check if all info are returned
    cursor.execute("SELECT * FROM bigbucks")

    # Extract and print data from query
    rows = cursor.fetchall()

    print("\nemp_no | salary")
    for r in rows:
        print(f"{r[0]} | {r[1]}")

    # Validate data in first row and all data length
    assert rows[0][0] == 10237
    assert rows[0][1] == 122275
    assert len(rows) == 2287
