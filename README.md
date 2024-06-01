# Information System
A food item, establishment, and review database management system.
## Running the application locally
Firstly, deploy or setup the MariaDB server in your terminal using the same directory in your repo. Make sure MariaDB and Python is installed in your local machine.

    $ mysql -u root -p
    Enter password: <password here>
    MariaDB [(none)]> source food.sql
    MariaDB [(none)]> exit


Next, install the necessary Python package needed to run the application.

    pip install mariadb

After setting up the food DB and installing the necessary package, run **app.py**

    python app.py

Or alternatively,

    python3 app.py

User credentials for logging-in is included in **user-credentials.txt**

## Developer guidelines
Always take note of the following notes.
1. **NEVER directly push nor edit main.** Before coding, always create a branch from the main branch.
2. **Add comments if applicable.** A comment is recommended if you cannot understand what a code block does with just a few seconds of reading.
3. **NEVER merge pull requests automatically.** 