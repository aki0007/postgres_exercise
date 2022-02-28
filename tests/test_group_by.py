import pytest
import datetime


@pytest.mark.parametrize("database", ["Employees"])
@pytest.mark.group_by
def test_how_many_people_are_hired_on_given_date(cursor_dict, database):
    """
    How many people were hired on did we hire on any given hire date?
    """
    query = """
    SELECT hire_date, COUNT(emp_no) as "amount"
    FROM employees
    GROUP BY hire_date
    ORDER BY "amount" DESC;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)
    # Extract and print data from query
    rows = cursor.fetchall()
    print("\nhire_date | amount")
    for r in rows:
        print(f"{r[0]} | {r[1]}")

    # Validate data in first row and all data length
    assert rows[0][0] == datetime.date(1985, 6, 20)
    assert rows[0][1] == 132
    assert len(rows) == 5434


@pytest.mark.parametrize("database", ["Employees"])
@pytest.mark.group_by
def test_show_employees_hired_after_1991_and_amount_of_positions(cursor_dict, database):
    """
    Show me all the employees, hired after 1991 and count the amount of positions they've had
    """
    query = """
    SELECT e.hire_date, count(t.title) as "amount of titles" 
    from employees as e
    Join titles as t using (emp_no)
    where extract(year from e.hire_date) > 1991
    group by e.emp_no
    ORDER BY e.emp_no;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)
    # Extract and print data from query
    rows = cursor.fetchall()
    print("\nhire_date | amount")
    for r in rows:
        print(f"{r[0]} | {r[1]}")

    # Validate data in first row and all data length
    assert rows[0][0] == datetime.date(1994, 9, 15)
    assert rows[0][1] == 1
    assert len(rows) == 87049


@pytest.mark.parametrize("database", ["Employees"])
@pytest.mark.group_by
def test_show_employees_from_development_and_from_to_date(cursor_dict, database):
    """
    Show me all the employees that work in the department development and the from and to date.
    """
    query = """
    SELECT e.emp_no, d.from_date, d.to_date 
    from employees as e
    join dept_emp as d using(emp_no)
    where d.dept_no = 'd005'
    GROUP BY e.emp_no, d.from_date, d.to_date
    ORDER BY e.emp_no, d.to_date;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)
    # Extract and print data from query
    rows = cursor.fetchall()
    print("\nemp_no | from_date | to_date")
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]}")

    # Validate data in first row and all data length
    assert rows[0][1] == datetime.date(1986, 6, 26)
    assert rows[0][2] == datetime.date(9999, 1, 1)
    assert rows[0][0] == 10001
    assert len(rows) == 85707
