###############################################################################
# built with <3 by flim.eth
#
# questions? reach out
# twitter.com/0xflim
# 0xflim@pm.me
#
# if this is helpful to you, please consider donating:
# 0x8d6fc57487ade3738c2baf3437b63d35420db74d (or flim.eth)
###############################################################################
import requests
import csv
import time
from datetime import datetime as dt

# declare fieldnames list
fieldnames = [
             'land_id'
            ,'image_url'
            ,'Category'
            ,'Sediment'
            ,'Sediment Tier'
            ,'Environment'
            ,'Environment Tier'
            ,'Eastern Resource'
            ,'Eastern Resource Tier'
            ,'Southern Resource'
            ,'Southern Resource Tier'
            ,'Western Resource'
            ,'Western Resource Tier'
            ,'Northern Resource'
            ,'Northern Resource Tier'
            ,'Artifact'
            ,'Koda'
            ,'Plot'
            ]

print(f'{dt.utcnow()} | {len(fieldnames)} number of field names\n')

# open the file in write mode, create writer, write header
f = open('/Users/flim/Desktop/otherdeeds.csv', 'w')
writer = csv.writer(f)
writer.writerow(fieldnames)

# set land_id & loop through ids thru final id 99999
land_id = 0
while land_id < 100000:
    try:
        value_list = []
        trait_list = []

        url = f'https://api.otherside.xyz/lands/{land_id}'
        r = requests.get(url)

        # check status code (404 probably means asset not minted)
        print(f'{dt.utcnow()} | checking asset number {land_id}...')

        # start with land_id
        trait_list.append('land_id')
        value_list.append(land_id)
        trait_list.append('image_url')

        if r.status_code == 404:
            # we probably found one that hasn't been minted
            print(f'{dt.utcnow()} | Status code: {r.status_code}')
            print(f'{dt.utcnow()} | Specified token number {land_id} has not been minted')
            print(f'{dt.utcnow()} | Backfilling data with "not_yet_minted"')

            # backfill all values with "not_yet_minted" except land_id
            for i in range(len(fieldnames)-1):
                value_list.append('not_yet_minted')
        else:
            print(f'{dt.utcnow()} | Status code: {r.status_code}')
            print(f'{dt.utcnow()} | asset number {land_id} found. Working...')
            print(f"{dt.utcnow()} | {len(r.json()['attributes'])} attributes on asset {land_id}")

            # add image_url value
            value_list.append(r.json()['image'])

            # iterate through asset's attributes & split into two lists
            for attr in r.json()['attributes']:	
                trait_list.append(attr['trait_type'])
                value_list.append(attr['value'])

            # check asset values against fieldnames, backfill with 'none'
            for i in range(len(fieldnames)):
                if fieldnames[i] != trait_list[i]:
                    trait_list.insert(i, fieldnames[i])
                    value_list.insert(i, 'none')

        print(f'{dt.utcnow()} | {value_list}\n')

        # write the data to file
        writer.writerow(value_list)

        land_id += 1
    except OSError as e:
        wait = 600
        print(f'{dt.utcnow()} | OSError: {e}')
        print(f'{dt.utcnow()} | Waiting {wait} seconds...\n')
        time.sleep(wait)

# close the file
f.close()