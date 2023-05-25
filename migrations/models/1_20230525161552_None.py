from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_name" VARCHAR(100) NOT NULL UNIQUE,
    "account_id" BIGINT NOT NULL UNIQUE,
    "name" VARCHAR(50) NOT NULL,
    "type" VARCHAR(10) NOT NULL,
    "image" BYTEA NOT NULL,
    "height" DOUBLE PRECISION,
    "weight" DOUBLE PRECISION
);
CREATE TABLE IF NOT EXISTS "target" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "begin" TIMESTAMPTZ NOT NULL  DEFAULT '25/05/2023',
    "end" TIMESTAMPTZ NOT NULL,
    "status" BOOL NOT NULL  DEFAULT False,
    "user_id_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
