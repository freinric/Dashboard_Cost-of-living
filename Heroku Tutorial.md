# Heroku deploy steps - Sophie

## Greate a Folder for your App
mkdir test_again
cd test_again

## Initialize the Folder
git init

## Create Virtual Environment
virtualenv venv

## Activate Virtual Environment
venv\Scripts\activate

## Add Files to venv
- .gitignore: what to ignore in your git
- Procfile: the command to execute your application
- requirements.txt: packages in your application
- py file: your application
- dataset

## Install Packages or venv
pip install dash
pip install plotly
pip install gunicorn

## Create Project on Heroku
heroku login
heroku create sophie-test-2

## Deploy App
git add .
git commit -m "Initial app"
git push heroku master

## Modify App
heroku git:clone -a sophie-test-2
cd sophie-test-2
git add .
git commit -am "Add slider"
git push heroku master



```python

```
