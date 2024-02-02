from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str

@dataclass
class JWTConfig:
    encoding_algorithm: str
    secret_key: str
    life_duration: int


@dataclass
class Config:
    db: DbConfig
    jwt: JWTConfig


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        jwt=JWTConfig(
            encoding_algorithm=env.str('JWT_ENCODING_ALGORITHM'),
            secret_key=env.str('JWT_SECRET_KEY'),
            life_duration=int(env.str('JWT_LIFE_DURATION'))
        )
    )
