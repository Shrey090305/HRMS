import pymysql
from tabulate import tabulate

# Connect to database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='dayflow_hrms'
)

cursor = conn.cursor()

print("\n" + "="*60)
print("DAYFLOW HRMS DATABASE OVERVIEW")
print("="*60)

# List all tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print(f"\n📊 Tables in database: {len(tables)}")
for table in tables:
    print(f"  - {table[0]}")

# Show record counts for each table
print("\n" + "="*60)
print("RECORD COUNTS")
print("="*60)
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  {table_name}: {count} records")

# Show sample data from each table
print("\n" + "="*60)
print("SAMPLE DATA (First 3 records from each table)")
print("="*60)

for table in tables:
    table_name = table[0]
    print(f"\n📋 {table_name.upper()}")
    print("-" * 60)
    
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
    rows = cursor.fetchall()
    
    if rows:
        # Get column names
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [col[0] for col in cursor.fetchall()]
        
        # Convert None to empty string for display
        clean_rows = [[str(cell) if cell is not None else '' for cell in row] for row in rows]
        
        # Print table
        print(tabulate(clean_rows, headers=columns, tablefmt="grid", maxcolwidths=20))
    else:
        print("  (No records)")

conn.close()

print("\n" + "="*60)
print("To query database manually, use MySQL command line:")
print("  mysql -u root -proot dayflow_hrms")
print("="*60)
