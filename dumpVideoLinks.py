import MySQLdb
import MySQLdb.cursors
import csv

db = MySQLdb.connect(host="mysql.server", user="joeacanfora", passwd="password",db="joeacanfora$CrowdStore")
c = db.cursor()
c.execute("""SELECT series_number, project_id, main_video_link FROM project_table WHERE series_number < 54;""")
result = c.fetchall()

file = csv.writer(open("video_links_first_30.csv","wb"))
headers = ('series_number', 'project_id', 'main_video_link')
file.writerow(headers)
for row in result:
    file.writerow(row)

print "file successfully created and written to."