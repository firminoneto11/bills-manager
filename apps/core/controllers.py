from conf.db import get_db_handler


class HealthCheckController:
    @staticmethod
    async def get():
        healthy = True
        try:
            await get_db_handler().ping()
        except ConnectionError:
            healthy = False

        return {"healthy": healthy}
