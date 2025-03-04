# Dexterity Interface

## Setup
1. First, create a python virtual environment in this directory:

    ```bash
    python3 -m venv venv
    ```


2. Next activate the python virtual environment
    ```bash
    # Linux/Mac:
    source venv/bin/activate  

    #Windows:
    .\venv\Scripts\Activate.ps1
    ```

    If this windows command doesn't work, you may have to run this in an Admin shell first:
    ```powershell
    set-executionpolicy remotesigned
    ```

3. Next, install all the python requirements:
    ```bash
    pip install -r requirements.txt
    ```


## Running

Note: if your venv has become deactivated, you may need to reactivate (step 2 in the Setup section)

* To run the reddit script, run:
    ```bash
    python3 reddit_with_comments.py
    ```

* To run the tiktok script, run:
    ```bash
    python3 tiktok.py
    ```

