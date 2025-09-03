from environs import Env

env = Env()
env.read_env()

class Settings:
    bot_token = env.str("BOT_TOKEN")
    admins_ids = env.list("ADMINS_IDS")
    db_name = env.str("POSTGRES_DB")
    db_user = env.str("POSTGRES_USER")
    db_password = env.str("POSTGRES_PASSWORD")
    db_host = env.str("POSTGRES_HOST")
    db_port = env.str("POSTGRES_PORT")
