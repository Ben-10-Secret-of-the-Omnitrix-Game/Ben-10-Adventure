
class BaseEntity:
    """
    What is Entity?
    Entity is everything that implies life creature or in simple words everything that's alive

    It's a base class of Entity

    I need my own entity, what should I do?
        Firstly, define class named by this rules:
            Your class name end with "Entity" (case sensetive)
        Next, inherit your class from BaseEntity whenever your entity is!

    """

    def __init__(self):
        pass


class Player(BaseEntity):
    """
    In singleplayer:
        Player is main adventurer. Trying to pass the game till the end
    In multiplayer:
        There are a lot of Players surronding you and bumbling around.

    """
    pass


class NPC(BaseEntity):
    """
    NPC -   all "zombie" like entities. 
    E.g. "players"(not exacly) that's attacking Player(main adventurer, see above). 
    How to know is it NPC?
        * Nonone control it with keyboard, mouse, any other stuff.
        * has primitive actions, generally it's stupid AI or hardcoded actions.
    """
    pass
