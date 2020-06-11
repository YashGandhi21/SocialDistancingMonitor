# SocialDistancingMonitor
Social Distancing Monitor Project

## For Flask Server Execution In windows cmd

**setup python virtual environment**

```
python -m venv venv

venv\Scripts\activate
```

**install dependencies**
```
pip install -r requirements.txt
```

**For Debug server execute**
```
python app.py
```

### OR

**For development server server execute**
```
flask run
```

**To exit from Virtual Environment**
```
deactivate
```

## For Flask Server Execution In Linux Terminal using virtualenv
make sure that virtualenv is installed by executing
```
pip3 freeze | grep virtualenv
```
if already **installed** it will show you the *version number*.else nothing will be printed <br />
if **Not** installed, then install by 
```
pip3 install virtualenv
```

**setup python virtual environment**

```
virtualenv venv

source venv/bin/activate
```

**install dependencies**
```
pip3 install -r requirements.txt
```

**For Debug server execute**
```
python3 app.py
```

### OR

**For development server server execute**
```
flask run
```

**To exit from Virtual Environment**
```
deactivate
```



