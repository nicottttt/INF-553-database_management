1) Create and populate the database pubmed
-- open a terminal (in windows, open powershell)
-- run "unzip Chuhao-tang-Alex-quach.zip" (if not install unzip, run "sudo apt-get install unzip")
-- run "cd Chuhao-tang-Alex-quach"
-- run "psql -U postgres"
-- enter your password for the user postgres
-- copy all the content from the file "init.sql" into the psql command line


2) Config the config file and run the server: 
-- run "cd django_postgres_site/django_postgres_site"
-- open config.ini (run "vim config.ini" or use other text editor)
-- change the "postgres_user_password" to the same password you logged in

-- run "cd ../inf553"
-- open config.ini (run "vim config.ini" or use other text editor)
-- change the "postgres_user_password" to the same password you logged in

-- run "cd ../.."
-- run "pip install psycopg2" if you don't have it
-- run "python manage.py runserver"

3) Use client to open the pages:
-- copy "http://127.0.0.1:8000/inf553/" to your browser
-- finish!


We have already tried to test all the procedures in another windows machine. 
If you have trouble in testing the above procedures in Linux, feel free to reach out to us!
chuhao.tang@polytechnique.edu 
alex.quach@polytechnique.edu