import os

# Postgres
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'workshop2022')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_MIN_SIZE = int(os.getenv('POSTGRES_MIN_SIZE', '1'))
POSTGRES_MAX_SIZE = int(os.getenv('POSTGRES_MAX_SIZE', '20'))

# node
ETHEREUM_NODE_URL = os.getenv('ETHEREUM_NODE_URL')
MESSAGE_STORAGE_CONTRACT_ADDRESS = os.getenv(
    'MESSAGE_STORAGE_CONTRACT_ADDRESS',
    '0x42307f34c15ef39718808588d4c2f9dcdb4e5900'
)

# Zerion API
ZERION_API_URL = os.getenv('ZERION_API_URL', 'wss://api-v4.zerion.io/')
ZERION_API_TOKEN = os.getenv('ZERION_API_TOKEN', 'Demo.ukEVQp6L5vfgxcz4sBke7XvS873GMYHy')
ZERION_API_TOKEN_ORIGIN = os.getenv('ZERION_API_TOKEN_ORIGIN', 'http://localhost:3000')
