from abc import ABC, abstractmethod


class ControllerContract(ABC):
    @abstractmethod
    async def get_all():
        pass

    @abstractmethod
    async def get_one(id: int):
        pass

    @abstractmethod
    async def store():
        pass

    @abstractmethod
    async def update(id: int):
        pass

    @abstractmethod
    async def delete(id: int):
        pass
