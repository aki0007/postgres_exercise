import pytest
import datetime


@pytest.mark.parametrize("database", ["Store"])
@pytest.mark.conditional_statement
def test_show_employees_hired_after_1991_having_more_then_two_titles(cursor_dict, database):
    """
    Create a case statement that's named "price class" where if a product is over 20 dollars you show 'expensive'
    if it's between 10 and 20 you show 'average'
    and of is lower than or equal to 10 you show 'cheap'.
    """
    query = """
    SELECT prod_id, price,
        CASE 
            WHEN price > 20 THEN 'expensive'
            WHEN price < 10 THEN 'cheap'
            WHEN price BETWEEN 10 AND 20 THEN 'average'
        END AS "price class"
    FROM products;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)
    # Extract and print data from query
    rows = cursor.fetchall()
    print("\nprod_id | price | price class")
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]}")

    # Validate data in first row and all data length
    assert rows[0][0] == 1
    assert float(rows[0][1]) == 25.99
    assert rows[0][2] == "expensive"
    assert len(rows) == 10000
