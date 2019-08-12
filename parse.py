import json, csv
import os, errno, glob, sys, smtplib, ssl
import time
import atexit
import logging

export_list = []

def find_element(element, JSON):     
  paths = element.split(".")
  data = JSON
  for i in range(0,len(paths)):
    data = data[paths[i]]
  return data

def get_json(name):
    with open('%s' % name) as json_file:
        return json.load(json_file)

def get_row(fileName):
    rawJson = get_json(fileName)
    timestamp = fileName[10:]
    timestamp = timestamp[:19]
    print(timestamp)
    row_dict = {'timestamp':timestamp, 'download':find_element("end.sum_received.bits_per_second", rawJson), 'upload':find_element("end.sum_sent.bits_per_second", rawJson)}
    return row_dict

def main():
    dir_list = glob.glob("iperfLogs/*.json")
    for s in dir_list:
        export_list.append(get_row(s))

    keys = export_list[0].keys()

    with open('log.csv', 'w') as output_file:
        keys = ['timestamp', 'download', 'upload']
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(export_list)

main()