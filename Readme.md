# Overview

This project is actually a collection of custom operators,hooks and sensors.

The example dag with this repo will be scheduled daily at 3.00 P.M IST and will try to fetch tweets from @diprjk twitter handle which is the Official Twitter handle of Department of Information and Public Relations, Govt of Jammu & Kashmir. The DAG uses a custom sensor to sense tweet related to daily COVID update of J&K.

When the tweet is found, the custom operator will download the update which is in the form of an image and saves it in locally for further analysis.

Then the operator will use a libary ExtractTable (https://extracttable.github.io/ExtractTable-py/) to convert the image into a dataframe.

And finally the dataframe is processed and converted into a structured csv file.

## Getting Started With Apache Airflow

Installation of airflow is simple, you can find installation details for airflow on the official website [airflow.apache.org](https://airflow.apache.org/docs/stable/start.html)

This plugins is tested with airflow v 1.10.9.
 
 if you have airflow allready installed then jump to [Step 12](#step12)

### Steps

1. We will be using virtualenv so make sure virtual env is installed

```bash
~$ pip install virtualenv
```
or

```bash
~$ pip3 install virtualenv
```
2. Create a new directory for our project like airflow_tweet_test or something you may wish
```bash
~$ mkdir airflow_tweet_test
```

3. cd into the newly created directory
```bash
~$ cd airflow_tweet_test
```

3. Use python virtualenv to create a virtual environment for our project 

```bash
~$ python -m virtualenv {name_of_virtual_env}
```
   where {name_of_virtual_env } is the name given to your virtual environment.

4. Airflow requires a special variable ``PATH`` variable with the name ``AIRFLOW_HOME`` it's necessary for your ``airflow`` to find the project files. Let's do it one by one.
 * Now use the following command to open an editor

```bash
~$ nano {project_path}/{name_of_virtual_env}/bin/activate
```

This will open a bash script, scroll to the end of the file and paste the following lines at the end of the file
where {project_path} is full path of your project and {name_of_virtual_env } is the name given to your virtual environment.
 ```bash

#This is for AIRFLOW usage
export AIRFLOW_HOME=/{project_path}
```

press CTRL+X and y, to close the editor

* You are ready to activate your virtual environment. enter the following command to activate it

```bash
~$ source ./{name_of_virtual_env}/bin/activate
```

5. Now install airflow using pip inside virtual env
```bash
~$ pip install apache-airflow==1.10.9
```
6. Check if airflow is sucessfully installed or not. Type following command inside terminal
 ```bash
~$ airflow version
```
if some error occurs like ``sqlalchemy.exc`` exception type following command
 
 ```bash
~$ pip install SQLAlchemy==1.3.15
~$ pip install Flask-SQLAlchemy==2.4.4
```

7. create a new folder ``plugins`` inside our project home
 ```bash
~$ mkdir plugins
```

8. Now clone this repo inside ``plugins`` directory 
 ```bash
~$ git clone https://
```
9. To install twitter_plugin dependencies, we prefer installation using ``requirements.txt`` file. Enter the following command to install  other dependent packages required for our twitter_plugin

```bash
~$ pip install -r /plugins/twitter_plugin/requirements.txt
```
10. Once all the dependencies are installed, its time to initialize your ``airflow`` meta-database

```bash
~$ airflow initdb
```

11. Once you have initialized your airflow db, you can start airflow webserver and scheduler

```bash
~$ airflow webserver
```


```bash
~$ airflow scheduler
```

#### Steps if airflow is allready installed
12. Now we need to add few required airflow variables and airflow connections using airflow UI.
- ``twitter_plugin`` requires a ``config`` variable (An Airflow Variable) which contains few details like:
    * ``twitter_account_id`` : twitter account id of @diprjk
    * ``email`` : Your Email Id for notifications related stuff
    *``find_param`` : The string on which the sensor senses if tweet related to covid update is avalaible or not
    *``since_id`` : Initially empty .But later will be automatically updated by DAG.
    * ``NOTE :`` Create an Airflow Variable named ``config`` using Airflow UI, with value as shown in below example.
    * ``example``: 
    ```json 
    {
    "frequency": "daily", 
    "twitter_account_id": 830669077022531584, 
    "email": "yourmail@domain.com", 
    "find_param": "Media Bulletin on Novel", 
    "since_id": 1388848538663088135
    }
    
- ``twitter_plugin`` Also requires a ``twitter_default`` connection (An Airflow Connection) which contains twitter API credentials (visit : https://developer.twitter.com/en/apply-for-access for more info):
    * ``consumer_key`` : Obtained from twitter developer account
    * ``consumer_secret`` : Obtained from twitter developer account
    *``access_token`` : Obtained from twitter developer account
    *``access_token_secret`` : Obtained from twitter developer account
    * ``NOTE :`` Create an Airflow Connection named ``twitter_default`` using Airflow UI, leave all fields blank put your twitter credentials inside extra field like shown below.
    * ``example``: 
    ```json
  {
  "consumer_key" : "xxxxxx",
  "consumer_secret":"xxxxxxxxxx",
  "access_token":"xxxxxxxxx",
  "access_token_secret":"xxxxxx"
  }
 - ``twitter_plugin`` Also requires a ``extract_table_default`` connection (An Airflow Connection) which contains ExtractTable API credentials (visit : https://extracttable.github.io/ExtractTable-py/):
    * ``password`` : ExtractTable API key 
    * ``NOTE :`` Create an Airflow Connection named ``extract_table_default`` using Airflow UI, leave all fields blank put your extracttable API key inside password field.
    
 13. Now copy ``dag_tweet_etl.py`` from ``twitter_plugin/example_dags/`` to ``project directory/dags``
 
 14. And we are good to go.



