from asyncpg.pool import Pool


class Base:
    def __init__(self, connection_pool: Pool) -> None:
        self.connection_pool = connection_pool
