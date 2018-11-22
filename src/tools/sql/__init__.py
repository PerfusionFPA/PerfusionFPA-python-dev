import MySQLdb as db
# TODO:  Implement SQL functionality, rather than relying on file directories.  This will allow
# for more efficient searching and organization, while leaving files in a 'flat' file system.

# TABLE TEMPLATES
patient_table = """CREATE TABLE patient (
PatientID varchar(100),
AcqDate date,
ProtocolType varchar(255),
FilterType varchar(255),
ReconType varchar(255),
KernelType varchar(255),
Path varchar(1000)
);
"""

# CONNECT TO SQL
conn = db.connect(host="localhost",
                  user="root",
                  passwd="",
                  db='patient_db',
                  )
cursor = conn.cursor()

# DETERMINE IF TABLES EXIST
table = 'patient'
_SQL = """SHOW TABLES"""
cursor.execute(_SQL)
results = cursor.fetchall()
print('All existing tables:', results)

results_list = [item[0] for item in results]

if table in results_list:
    print('Current table exists')
else:
    print('Current table doesnt exist')
    cursor.execute(patient_table)
    
# CLOSE CONNECTION TO SQL
cursor.close()
conn.close()