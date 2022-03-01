import pytest
import datetime


@pytest.mark.parametrize("database", ["movr"])
@pytest.mark.mystery
def test_mystery_step_one(cursor_dict, database):
    """
    Create a view suspected_rides which narrows suspected rides selection:
    """
    view = """
    CREATE OR REPLACE VIEW suspected_rides AS
    SELECT * FROM vehicle_location_histories AS vlh 
    WHERE 
        city = 'new york' AND 
        long BETWEEN 40.5 AND 40.6 AND
        lat BETWEEN -74.997 AND -74.9968 AND 
        vlh.timestamp::date = '2020-06-23'::date
    ORDER BY long;
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(view)
    # Execute view
    cursor.execute("SELECT * FROM suspected_rides")
    # Extract and print data from query
    rows = cursor.fetchall()

    # Validate data length
    assert len(rows) == 428


@pytest.mark.parametrize("database", ["movr"])
@pytest.mark.mystery
def test_mystery_step_two(cursor_dict, database):
    """
    Join rides and users with suspected_rides
    """
    query = """
    SELECT DISTINCT r.vehicle_id, u.name as "Rider name", u.address 
    FROM suspected_rides AS vlh
    JOIN rides AS r ON r.id = vlh.ride_id
    JOIN users as u ON u.id = r.rider_id
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Execute query
    cursor.execute(query)
    # Extract and print data from query
    rows = cursor.fetchall()

    # Validate data length
    assert len(rows) == 109


@pytest.mark.parametrize("database", ["movr"])
@pytest.mark.mystery
def test_mystery_step_three(cursor_dict, database):
    """
    Create view suspect_riders_name that will be used as table to help reduce suspects.
    Create dblink to link movr and employees DB
    """
    view = """
    CREATE OR REPLACE VIEW suspect_riders_name AS
    SELECT DISTINCT
        split_part(u.name, ' ', 1) AS "first_name",
        split_part(u.name, ' ', 2) AS "last_name"
    FROM suspected_rides AS sr
    JOIN rides AS r ON r.id = sr.ride_id
    JOIN users as u ON u.id = r.rider_id
    """
    # Choose DB to execute queries on
    cursor = cursor_dict[database]
    # Create view
    cursor.execute(view)
    # Execute query
    cursor.execute("SELECT * FROM suspect_riders_name")
    # Extract and print data from query
    rows = cursor.fetchall()

    # Validate data length
    assert len(rows) == 103

    # Create a DB link
    db_link = """
    SELECT DISTINCT
        CONCAT(t1.first_name , ' ', t1.last_name) AS "employee",
        CONCAT(u.first_name , ' ', u.last_name) AS "rider"
    FROM dblink('host=localhost user=postgres password=postgres dbname=Employees', 'SELECT first_name, last_name FROM employees;')
    AS t1(first_name NAME, last_name NAME)
    JOIN suspect_riders_name as u ON t1.last_name = u.last_name
    ORDER BY "rider" 
    """

    cursor.execute(db_link)
    rows = cursor.fetchall()

    # Validate data length
    assert len(rows) == 482

    # TODO: solution should be 11 :(
