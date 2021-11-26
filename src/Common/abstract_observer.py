from abc import ABC, abstractmethod

class AbstractObserver(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def update_state(self):
        """
        Updates the observers knowledge of the game state
        """
        pass
    
    @abstractmethod
    def render_view(self):
        """
        Renders the game state
        """
        pass