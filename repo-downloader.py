#Import Libraries
import platform
import math
import requests
import subprocess
import os

# Paste your Access token here
# To create an access token - https://github.com/settings/tokens
token = "access_token=" + "access_token"

# Base API Endpoint
base_api_url = 'https://api.github.com/'

# Enter the Username or the Organization name to download the Repositories
# Ex: machine+learning to search for Machine Learning
print('Enter the username ')

username = input()
print('\n Username entered is', username, '\n')

# URL Endpoint to get User Info - mainly the number of Repositories
user_info_url = base_api_url + "users/" + username

# Base URL Endpoint to Access Repository Data
repository_base_url = base_api_url + "users/" + username + "/repos?" + token

# Hit the User Info API Endpoint and get the JSON response
user_info_request = requests.get(user_info_url)

if user_info_request.status_code != 200:
    print ("Username doesn't exist. Please check for spelling mistake")

else:

    # Check the OS Name to make compatible shell script
    if platform.platform() != "Windows":
        file_name = "git-clone.sh"
    else:
        file_name = "git-clone.bat"


    user_info_response = user_info_request.json()

    # Check for the number of repositories of the user
    no_of_repositories = user_info_response['public_repos']

    # Calculate the number of pages to for pagination
    # A JSON request for the User repo data contains only 30 projects. 
    # Dividing the repos by 30 and ceiling it shows the number of requests to be made
    pages = int(math.ceil(no_of_repositories / 30.0))
    print ("No of Repositories for {0} is {1}".format(username, no_of_repositories))

    # Create an empty file to store the clone URL's and then execute it 
    file = open(file_name, 'w')
    file.close()

    # Iterate over the pagination for the requests
    for page in range(1, pages + 1):
        
        # Create a paginated URL to get Repository Data
        page_url = repository_base_url + "&page=" + str(page)
        
        # Hit the generated paginated URL and get the JSON Response
        page_response = requests.get(page_url).json()

        # Since all the JSON requests won't have same number of repositores in them
        # We calculate the number of repositores and iterate accourdingly and store it in the shell script
        for i in range(len(page_response)):
            print (page_response[i]['clone_url'])
            file = open(file_name, 'a')
            file.write('git clone ' + page_response[i]['clone_url'] + "\n")
            file.close()      
    
    #Subprocess System call to execute the script file and start the cloning process
    subprocess.check_output(['chmod', 'a+x', file_name])
    subprocess.check_output('./'+file_name, shell=True)

    #Delete the script file after cloning
    os.remove(file_name)

