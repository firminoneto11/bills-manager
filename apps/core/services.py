from conf.db import get_database


class HealthCheckService:
    async def check_resources(self):
        healthy = {
            "healthy": True,
            "resources": {
                "database_healthy": True,
                "redis_healthy": True,  # NOTE: Implement these as the need arises
            },
        }

        try:
            await get_database().ping()
        except ConnectionError:
            healthy["resources"]["database_healthy"] = False

        healthy["healthy"] = all(healthy["resources"].values())

        return healthy
