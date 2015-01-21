import requests

#redirect my user to venmo first

data = {
	'client_id': '2284',
	'scope': 'access_profile',
	'response_type': 'code',
	'client_secret': '4L23sdF428pwBQYrMe3UQKrdQpdC4GvC'
}

url = 'https://api.venmo.com/v1/oauth/authorize'

response = requests.post(url, data, auth=('mpneary5@gmail.com','Xsw2Zaq1'), allow_redirects=True)

print response.status_code
'''
data ['client_id'] = 2284
data ['client_secret'] = '4L23sdF428pwBQYrMe3UQKrdQpdC4GvC'
data ['code'] = 'us5wYnh7rtKQXcFS9ZrHDMBaAEEBxcNH'
data ['scope'] = 'make_payments'
data ['response_type'] = 'code'


url = 'https://api.venmo.com/v1/oauth/access_token'

response = requests.post(url, data)

print response.json()
'''
