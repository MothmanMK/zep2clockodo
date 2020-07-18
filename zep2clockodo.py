#!/usr/bin/env python3

import os, sys, json, glob, argparse, configparser
from datetime import datetime, timedelta

import pandas, requests

ini_path = os.path.abspath(os.path.dirname(sys.argv[0]))

#config Datei im gleichen Verzeichnis ausfindig machen
configparser = configparser.RawConfigParser()
configFilePath = ini_path + '/' + 'config.ini'
configparser.read(configFilePath)

#Loginwerte
var_clockodo_api = configparser.get('Login', 'api key')
var_clockodo_user = configparser.get('Login', 'user')
var_user_id = configparser.get('Login', 'user id')

#Variabeln fuer die richtigen Projektzuordnung
ProjectIdentfier1 = configparser.get('ProjectIdentfier', 'ProjectIdentfier1')
ProjectIdentfier2 = configparser.get('ProjectIdentfier', 'ProjectIdentfier2')
ProjectIdentfier3 = configparser.get('ProjectIdentfier', 'ProjectIdentfier3')
ProjectIdentfier4 = configparser.get('ProjectIdentfier', 'ProjectIdentfier4')
ProjectIdentfier5 = configparser.get('ProjectIdentfier', 'ProjectIdentfier5')
ProjectIdentfier6 = configparser.get('ProjectIdentfier', 'ProjectIdentfier6')
ProjectIdentfier7 = configparser.get('ProjectIdentfier', 'ProjectIdentfier7')

#Code fuer die Projekte
def Project1():
    global var_projects_id, var_customer_id, var_services_id, var_billable
    var_projects_id = configparser.get('Project1', 'Project ID')
    var_customer_id = configparser.get('Project1', 'Customer ID')
    var_services_id = configparser.get('Project1', 'Services ID')
    var_billable = configparser.get('Project1', 'Billable')

def Project2():
    global var_projects_id, var_customer_id, var_services_id, var_billable
    var_projects_id = configparser.get('Project2', 'Project ID')
    var_customer_id = configparser.get('Project2', 'Customer ID')
    var_services_id = configparser.get('Project2', 'Services ID')
    var_billable = configparser.get('Project2', 'Billable')

def Project3():
    global var_projects_id, var_customer_id, var_services_id, var_billable
    var_projects_id = configparser.get('Project3', 'Project ID')
    var_customer_id = configparser.get('Project3', 'Customer ID')
    var_services_id = configparser.get('Project3', 'Services ID')
    var_billable = configparser.get('Project3', 'Billable')

def Project4():
    global var_projects_id, var_customer_id, var_services_id, var_billable
    var_projects_id = configparser.get('Project4', 'Project ID')
    var_customer_id = configparser.get('Project4', 'Customer ID')
    var_services_id = configparser.get('Project4', 'Services ID')
    var_billable = configparser.get('Project4', 'Billable')

def Project5():
    global var_projects_id, var_customer_id, var_services_id, var_billable
    var_projects_id = configparser.get('Project5', 'Project ID')
    var_customer_id = configparser.get('Project5', 'Customer ID')
    var_services_id = configparser.get('Project5', 'Services ID')
    var_billable = configparser.get('Project5', 'Billable')

def Project6():
    global var_projects_id, var_customer_id, var_services_id, var_billable
    var_projects_id = configparser.get('Project6', 'Project ID')
    var_customer_id = configparser.get('Project6', 'Customer ID')
    var_services_id = configparser.get('Project6', 'Services ID')
    var_billable = configparser.get('Project6', 'Billable')

def Project7():
    global var_projects_id, var_customer_id, var_services_id, var_billable
    var_projects_id = configparser.get('Project7', 'Project ID')
    var_customer_id = configparser.get('Project7', 'Customer ID')
    var_services_id = configparser.get('Project7', 'Services ID')
    var_billable = configparser.get('Project7', 'Billable')

def raw_entries_cli():
    global df
    global file_path
    parser = argparse.ArgumentParser(description='Adds entries to Clockodo from a xls/xlsx file')
    parser.add_argument('file_path')
    args = parser.parse_args()
    df = pandas.read_excel(args.file_path)

def raw_entries_search():
    global df
    global file_path
    filelist = glob.glob(ini_path + '/*.xls', recursive=False)
    if filelist == []:
        sys.exit('No file found.')
    file_path = filelist[0]
    df = pandas.read_excel(file_path)

def find_latest_online_entry():
    global latest_entry
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    then = datetime.today() - timedelta(35)
    then = then.strftime('%Y-%m-%d %H:%M:%S')
    response = requests.get("https://my.clockodo.com/api/entries",
                            headers={
                                "X-ClockodoApiUser": var_clockodo_user,
                                "X-ClockodoApiKey": var_clockodo_api, },

                            params={
                                "time_since": then,
                                "time_until": now,
                                "filter[users_id]": var_user_id, },
                            )
    jresp = json.loads(response.text)  # load from json to object
    jresp = (jresp["entries"])  # remove groups above entries
    jresp = pandas.DataFrame.from_dict(jresp)  # turn into a dataframe/dictionary
    jresp = jresp["time_until"]  # remove all columns except time_until
    latest_entry = pandas.DataFrame.max(jresp)  # show the highest value in the dataframe
    # pandas.to_datetime(latest_entry, unit='ns')
    latest_entry = pandas.to_datetime(latest_entry, format='%Y-%m-%d %H:%M:%S')
    print("Latest entry in Clockodo until:", latest_entry)

def trim_raw_entries():
    global df
    # Zählt alle Zeilen
    maxrows_before = int(len(df.index))

    indexes_to_drop = []

    for line in range(0, maxrows_before):
        if latest_entry > pandas.to_datetime(df.iloc[line, 0], format='%Y-%m-%d %H:%M:%S'):
            indexes_to_drop.append(line)
    df.drop(df.index[indexes_to_drop], inplace=True)
    maxrows_after = int(len(df.index))
    print("Result for entries:", maxrows_before, "found.", "Sending", maxrows_after, "omitting", maxrows_before - maxrows_after)

def sendto_clockodo():
    #Zählt alle Zeilen
    maxrows = int(len(df.index))
    print("Sending...")
    for line in range(0, maxrows):
        # Variable Werte je nach Eintrag aus ZE
        var_text = df.Task.values[line]
        var_time_since = pandas.DataFrame(df).iloc[line, 0].strftime('%Y-%m-%d %H:%M:%S')
        var_time_until = pandas.DataFrame(df).iloc[line, 1].strftime('%Y-%m-%d %H:%M:%S')

        var_projects_name = df.Kunde.values[line]
        # Wenn Feld ZE-Kunde eines dieser trifft, dann entsprechen Werte für Kunden/Projekt nehmen
        # Achtung, das ist nur ein Teil des eigentlich Clockodo-Projektnamens
        if ProjectIdentfier1 in var_projects_name:
            Project1()

        elif ProjectIdentfier2 in var_projects_name:
            Project2()

        elif ProjectIdentfier3 in var_projects_name:
            Project3()

        elif ProjectIdentfier4 in var_projects_name:
            Project4()

        elif ProjectIdentfier5 in var_projects_name:
            Project5()

        elif ProjectIdentfier6 in var_projects_name:
            Project6()

        elif ProjectIdentfier7 in var_projects_name:
            Project7()

        #### Festlegen der Daten für Übergabe
        entry = {
            "time_since": var_time_since,
            "time_until": var_time_until,
            "customers_id": var_customer_id,
            "services_id": var_services_id,
            "projects_id": var_projects_id,
            "billable": var_billable,
            "text": var_text,

        }

        response = requests.post("https://my.clockodo.com/api/entries", json=entry,
                             headers={
                                 "X-ClockodoApiUser": var_clockodo_user,
                                 "X-ClockodoApiKey": var_clockodo_api,
                             }
                             )

        print("Entry", line, "(", var_time_since, ")", response)


def cleanup():
    print("All done!")
    os.remove(file_path)
    print(file_path, "deleted.")


#raw_entries_cli()

raw_entries_search()
find_latest_online_entry()
trim_raw_entries()
sendto_clockodo()
cleanup()
