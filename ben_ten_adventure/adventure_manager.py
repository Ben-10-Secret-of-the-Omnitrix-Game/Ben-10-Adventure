
class Adventure:
    """
    Base class for every adventure.
    * Any adventure must inherit be inherited from it.
    """
    pass
        

class AdventureManager:
    """
    Manages adventure list
    Has properties:
        name    -   somehow displayed name of adventure
        config  -   configuration file. Instance of ben_ten_adventure.utils.config.Config
                    Config should contain information about (asset files, ... will exand soon) 

        that's all by now
    """
    pass

class SecretOfTheOmnitrix(Adventure):
    def __init__(self):
        self.stages = [
            self.show_intro,
            self.start_scene_1,
            self.show_intro_2,
            self.start_scene_2,
            self.start_scene_3]
        
    def show_intro(self):
        """
        First video. 
        """
        pass
    
    def start_scene_1(self):
        """
        Fight between Ben 10 and prisoners. Save Myaxx
        """
        pass
    
    def show_intro_2(self):
        """
        Flying to Azmuth's planet
        """
        pass
    
    def start_scene_2(self):
        """
        Fighting with Vilgax
        """
        pass
    
    def start_scene_3(self):
        """
        Urge Azmuth to keep omnitrix in Ben's hand.  
        """
        pass
    
    