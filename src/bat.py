import uuid

ATTRIBUTES = (
    "enemy",
    "player",
)

class Battle:
    """
    Battle.
    """
    
    def __init__(self, save_data) -> None:
        if save_data is None:
            save_data = dict()

        self.instance_id = uuid.uuid4()
        self.enemy = ""
        self.player = ""
        self.outcome = OutputBattle.draw
        self.steps = 0

        self.set_state(save_data)

    def get_state(self):
    
        save_data = {
            attr: getattr(self, attr)
            for attr in SIMPLE_PERSISTANCE_ATTRIBUTES
            if getattr(self, attr)
        }

        save_data["instance_id"] = str(self.instance_id.hex)

        return save_data

    def set_state(self, save_data) -> None:
    
        if not save_data:
            return

        for key, value in save_data.items():
            if key == "instance_id" and value:
                self.instance_id = uuid.UUID(value)
            elif key in SIMPLE_PERSISTANCE_ATTRIBUTES:
                setattr(self, key, value)
                
    def enemy_damaged(self):
        """
        Return text of enemy being hit using calculated damage.
        """
        return "Enemy hit with {} damage.".format(self.enemy_damage)
    
    def set_enemy_damage(self, enemy_damage):
         
        self.enemy_damage = enemy_damage
        self.state_dict[c.ENEMY_DAMAGED] = self.enemy_damaged()
        
    def set_player_damage(self, player_damage):
        """
        Set player damage in state dictionary.
        """
        self.player_damage = player_damage
        self.state_dict[c.PLAYER_DAMAGED] = self.player_hit()

    def player_hit(self):
        if self.player_damage:
            return "Player hit with {} damage".format(self.player_damage)
        else:
            return "Enemy missed!"
        
    def update(self):
        """Updates info box"""
        self.image = self.make_image()
        
    @property
     
    def rect(self):
        
        return self.image.get_rect(centerx=self.posx, bottom=self.posy)

    def draw(self, surface):
        """
        Draw to surface.
        """
        surface.blit(self.image, self.rect)



