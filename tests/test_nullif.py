import pytest


@pytest.mark.parametrize("database", ["Store"])
@pytest.mark.nullif
def test_how_many_people_are_hired_on_given_date(cursor_dict, database):
    """
    Show NULL when the product is not on special (0)
    """
    query = """
    SELECT prod_id, title, price, NULLIF(special, 0) as "special"
    FROM products
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)
    # Extract and print data from query
    rows = cursor.fetchall()
    print("\nprod_id | title |price |special")
    for r in rows:
        print(f"{r[0]} | {r[1]}| {r[2]} | {r[3]}")

    # Validate data in first row
    assert rows[0][0] == 1
    assert rows[0][1] == "ACADEMY ACADEMY"
    assert float(rows[0][2]) == 25.99
    assert rows[0][3] is None

    # Validate data in fifth row and all data length
    assert rows[4][0] == 5
    assert rows[4][1] == "ACADEMY AFRICAN"
    assert float(rows[4][2]) == 11.99
    assert rows[4][3] == 1
    assert len(rows) == 10000
