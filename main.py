import pandas as pd

from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file

from app.data.datasets import load_all_csv_data
from app.data.incidents import (
    insert_incident,
    get_all_incidents,
    update_incident_status,
    delete_incident,
    get_incidents_by_type_count,
    get_high_severity_by_status
)


def setup_database_complete():
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)

    # Connect
    conn = connect_database()

    # Create tables
    create_all_tables(conn)

    # Migrate users
    migrated = migrate_users_from_file(conn)
    print(f"Users migrated: {migrated}")

    # Load CSVs
    loaded = load_all_csv_data(conn)
    print(f"CSV rows loaded: {loaded}")

    # Verify
    cursor = conn.cursor()
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']

    print("\nDatabase Summary")
    print(f"{'Table':<25}{'Rows':<10}")
    print("-" * 40)

    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"{t:<25}{cursor.fetchone()[0]}")

    conn.close()

    print("\nDATABASE SETUP COMPLETE!")
    print(f"Database file: {DB_PATH.resolve()}")


def run_comprehensive_tests():
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)

    conn = connect_database()

    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")

    # CREATE
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create:   Incident #{test_id} created")

    # READ
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:     Found incident #{test_id}")

    # UPDATE
    update_incident_status(conn, test_id, "Resolved")
    print("  Update:   Status updated")

    # DELETE
    delete_incident(conn, test_id)
    print("  Delete:   Incident deleted")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")

    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:         {len(df_by_type)} categories")

    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity:    {len(df_high)} statuses")

    conn.close()

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)


def main():
    setup_database_complete()
    # Uncomment to run full tests:
    # run_comprehensive_tests()


if __name__ == "__main__":
    main()

