#import required modules
import requests
import pprint
import requests
import math
import subprocess
import os
import sys

#part 1 of the URL
part1 = 'https://api.github.com/users/'
#part 2 of the URL
part2 = '/repos'

print '\n'
print 'Enter the name Github username of the user to download the repo '

name = raw_input()
print "\n Username entered is", name, "\n"

#User profile URL
user_info = part1 + name
#User Repos URL
repo_url = user_info + part2

#GET request to get the user profile data in JSON
user_info_json = requests.get(user_info)	
#GET request to get the user repos data in JSON
json_req = user_info_json.json()

#Parse through the request and return the value of the no of repos of the user
repos = json_req['public_repos']
print 'No of repositories linked with the account is ', repos
#A JSON request for the User repo data contains only 30 projects. Dividing the repos by 30 and ceiling it shows the number of requests to be made
pages = int(math.ceil(repos / 30.0))	
print 'No of pages = ', pages

#Creates an empty file which will be passed on to the for loop to get all the Git clone commands
file = open('git-clone.sh', 'w')
file.close()

#Range of for to be set dynamically by the no of pages so as to send as many requests
for i in range(1, pages + 1):
	#Passing a parameter of page to get the JSON data for subsequent pages
    page_url = repo_url + '?page=' + str(i)
    full_repos = requests.get(page_url)
    full_repos_json = full_repos.json()
    length = len(full_repos_json)

    # print "Length of json is ", length
	#All the requests usually contain 30 repo details. The last page will can have details from 1 to 30 repos, hence we calculate the length dynamically so as to not encounter Out of bounds indec issue
    for j in range(0, length):
        file = open('git-clone.sh', 'a')
        file.write('git clone ')
        file.write(full_repos_json[j]['clone_url'])
        file.write('\n')
        file.close()

#Subprocess System call to execute the batch file and start the cloning process
subprocess.call('git-clone.sh', shell=True)
#Delete the batch file after cloning
os.remove('git-clone.sh')