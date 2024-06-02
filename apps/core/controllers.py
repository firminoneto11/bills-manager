from .services import HealthCheckService


class HealthCheckController:
    @staticmethod
    async def get():
        svc = HealthCheckService()
        return await svc.check_resources()
