from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    url: str

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
            url=f"postgresql+asyncpg://{env.str('DB_USER')}:{env.str('DB_PASS')}@{env.str('DB_HOST')}:5432/{env.str('DB_NAME')}",
        ),
        jwt=JWTConfig(
            encoding_algorithm=env.str('JWT_ENCODING_ALGORITHM'),
            secret_key=env.str('JWT_SECRET_KEY'),
            life_duration=int(env.str('JWT_LIFE_DURATION'))
        )

    )
