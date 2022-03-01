import pytest


@pytest.mark.parametrize("database", ["Store"])
@pytest.mark.subquery
def test_subquery_select_orders_by_customers_state(cursor_dict, database):
    """
    Get all orders from customers who live in Ohio (OH), New York (NY) or Oregon (OR) state
    """
    query = """
    SELECT concat(c.firstname, c.lastname) as "Name", o.orderid 
    FROM orders AS o, (
        SELECT customerid, state, firstname, lastname
        FROM customers
    ) AS c
    WHERE  o.customerid = c.customerid AND 
    c.state IN ('NY', 'OH', 'OR')
    ORDER BY o.orderid;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)

    # Extract and print data from query
    rows = cursor.fetchall()

    print("\nName | orderid")
    for r in rows:
        print(f"{r[0]} | {r[1]}")

    # Validate data in first row and all data length
    assert rows[0][0] == "OVPMOPLIZZSSPEUH"
    assert rows[0][1] == 21

    assert len(rows) == 359


@pytest.mark.parametrize("database", ["Employees"])
@pytest.mark.subquery
def test_subquery_filter_employees_with_specific_manager(cursor_dict, database):
    """
    Question: Filter employees who have emp_no 110183 as a manager
    """
    query = """
    SELECT emp_no, concat(first_name, ' ', last_name) as "Name"
    FROM employees
    WHERE emp_no IN (
        SELECT emp_no
        FROM dept_emp
        WHERE dept_no = (
            SELECT dept_no 
            FROM dept_manager
            WHERE emp_no = 110183
        )
    )
    ORDER BY emp_no
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)

    # Extract and print data from query
    rows = cursor.fetchall()

    print("\nemp_no | name")
    for r in rows:
        print(f"{r[0]} | {r[1]}")

    # Validate data in first row and all data length
    assert rows[0][0] == 10005
    assert rows[0][1] == "Kyoichi Maliniak"
    assert len(rows) == 17786
