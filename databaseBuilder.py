import MySQLdb

db = MySQLdb.connect(host="mysql.server", user="joeacanfora", passwd="password",db="joeacanfora$CrowdStore")
c = db.cursor()

c.execute("""DROP TABLE IF EXISTS rewards_table, project_updates_table, author_table, project_table CASCADE""")

#create project table
c.execute("""CREATE TABLE project_table (series_number MEDIUMINT NOT NULL AUTO_INCREMENT,
project_id VARCHAR(50), project_name VARCHAR(255), project_url VARCHAR(255), status VARCHAR(25),
goal VARCHAR(15), end_date DATE, author_name VARCHAR(255), location VARCHAR(255),
main_video_link VARCHAR(255), category VARCHAR(255), currency VARCHAR(5), graded1 BOOL, grader1PID VARCHAR(25),
firmid VARCHAR(50),
videopressent BOOL, videoquaility1 TINYINT, othcompreference1 TINYINT,
othcompname1 VARCHAR(50), pitchfocus1 TINYINT, founderschool1 BOOL,
founderschoolname1 VARCHAR(50), founderstartup1 BOOL,
founderstartupname1 VARCHAR(50), prototypes1 BOOL,
endorsements1 BOOL, endorsementname1 VARCHAR(50),
graded2 BOOL, grader2PID VARCHAR(25), videoquaility2 TINYINT, othcompreference2 TINYINT,
othcompname2 VARCHAR(50), pitchfocus2 TINYINT, founderschool2 BOOL,
founderschoolname2 VARCHAR(50), founderstartup2 BOOL,
founderstartupname2 VARCHAR(50), prototypes2 BOOL,
endorsements2 TINYINT, endorsementname2 VARCHAR(50), PRIMARY KEY(series_number))""")

#create rewards table
c.execute("""CREATE TABLE rewards_table (reward_id MEDIUMINT NOT NULL AUTO_INCREMENT, series_number MEDIUMINT NOT NULL,
pledge_amount DECIMAL(64,2), num_backers INT, delivery DATE, description VARCHAR(255), limited BOOL,
max_limit INT, PRIMARY KEY (reward_id), FOREIGN KEY (series_number) REFERENCES project_table(series_number))""")

#create project_updates_table
c.execute("""CREATE TABLE project_updates_table (update_id INT NOT NULL AUTO_INCREMENT, series_number MEDIUMINT NOT NULL,
pledged DECIMAL(64,2), num_backers INT, days_to_go INT, date DATE, PRIMARY KEY (update_id),
FOREIGN KEY (series_number) REFERENCES project_table(series_number))""")

#create author_table
c.execute("""CREATE TABLE author_table (author_id INT NOT NULL AUTO_INCREMENT, series_number MEDIUMINT NOT NULL,
location VARCHAR(255), name VARCHAR(150), description VARCHAR(255), contact VARCHAR(50),
PRIMARY KEY(author_id), FOREIGN KEY (series_number) REFERENCES project_table(series_number))""")

c.execute("""SHOW TABLES FROM joeacanfora$CrowdStore""")
print c.fetchall()
