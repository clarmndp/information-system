# Information System
A food item, establishment, and review database management system using MariaDB and Python.
## Running the application locally
Firstly, deploy or run the MariaDB server in your terminal in the same directory as the repo. Make sure that MariaDB is installed on your local machine.

    $ mysql -u root -p
    Enter password: <password here>
    MariaDB [(none)]> source food.sql
    MariaDB [(none)]> exit
    
After setting up, run **app.py**

    python app.py

Or alternatively,

    python3 app.py

## Developer guidelines
Always take note of the following notes.
1. **NEVER directly push nor edit main.** Before coding, always create a branch from the main branch.
2. **Add comments if applicable.** A comment is recommended if you cannot understand what a code block does with just a few seconds of reading.
3. **NEVER merge pull requests automatically.** 
