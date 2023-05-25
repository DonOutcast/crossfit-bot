

DATABASE_CONFIG = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': 'localhost',
                'port': '5432',
                'user': 'postgres',
                'password': 'postgres',
                'database': 'postgres',
            }
        },
    },
    'apps': {
        'models': {
            'models': [
                "src.telegram_bot.model.database.models",
                "aerich.models",
            ],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'Europe/Moscow'
}
