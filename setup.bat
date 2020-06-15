@ECHO OFF 
:: This batch file setup Virtual Environment on local system
TITLE Virtual Environment Setup
:: Assuming python is already installed on pc
ECHO THIS IS ONE TIME ACTIVITY TO SETUP THE APPLICATION
ECHO Press Enter to setup virtual environment for python
PAUSE
ECHO Setting up Virtual Environment
python -m venv venv
ECHO Virtual Environment is set
ECHO Press Enter to install dependencies
PAUSE
ECHO Insatalling dependencies
CALL venv\Scripts\pip install -r requirements.txt
ECHO Dependencies are installed
where venv\Scripts\pip
PAUSE
ECHO Printing all installed modules
pip freeze
ECHO These modules are installed
PAUSE


