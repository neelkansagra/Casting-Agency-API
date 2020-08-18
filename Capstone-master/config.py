import os
database = {
    "database_name": "casting",
    "username": "postgres",
    "username_password": "abcd",
    "port": "localhost:5432"
}

Authtoken = {
 'casting_assistant': os.environ['CASTING_ASSISTANT'],
 'casting_director': os.environ['CASTING_DIRECTOR'],
 'executive_director': os.environ['EXECUTIVE_DIRECTOR']
}

auth_config = {
    'AUTH0_DOMAIN': os.environ['AUTH0_DOMAIN_NAME'],
    'ALGORITHMS': 'RS256',
    'API_AUDIENCE': os.environ['API_AUDIENCE'],
    'AUTH0_CLIENT_ID': os.environ['CLIENT_ID'],
    'AUTH0_CALLBACK_URL': os.environ['CALLBACK_URL']
}
