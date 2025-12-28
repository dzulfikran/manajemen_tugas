from abc import ABC, abstractmethod
from auth.domain.entities.entities import User

class BaseRepository(ABC):
    @abstractmethod
    def add(self, entity): pass

    @abstractmethod
    def update(self, entity): pass
    
    @abstractmethod
    def delete_by_id(self, id: str): pass
    
    @abstractmethod
    def get_all(self): pass
    
    @abstractmethod
    def get_by_id(self, id: str): pass

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_username(self, username: str) -> User:
        raise NotImplementedError