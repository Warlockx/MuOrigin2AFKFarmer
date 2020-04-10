import cv2


class Detection:
    def __init__(self, monitor):
        self.monitor = monitor
        self.resources = self.load_resources()

    def load_resources(self):
        return {
            'afk_screen': self.monitor.get_template('afk_screen.png'),
            'battle_off': self.monitor.get_template('auto_battle_off.png'),
            'battle_on': self.monitor.get_template('auto_battle_on.png'),
            'back_button': self.monitor.get_template('back_button.png'),
            'chat_collapse': self.monitor.get_template('chat_collapse_button.png'),
            'death_counter': self.monitor.get_template('death_counter.png'),
            'event_reference': self.monitor.get_template('event_reference.png'),
            'mail_icon': self.monitor.get_template('mail_icon.png'),
            'yellow_close_button': self.monitor.get_template('yellow_close_button.png'),
            'orange_close_button': self.monitor.get_template('orange_close_button.png'),
            'monster_icon': self.monitor.get_template('monster_icon.png')
        }

    def check_battle(self):
        battle_off = self.monitor.get_cords(self.resources['battle_off'])
        if battle_off:
            return False, battle_off
        elif self.monitor.get_cords(self.resources['battle_on']):
            return True, None
        else:
            return None, None

    def check_afk(self):
        return self.monitor.get_cords(self.resources['afk_screen'])

    def check_back_button(self):
        return self.monitor.get_cords(self.resources['back_button'])

    def check_chat(self):
        return self.monitor.get_cords(self.resources['chat_collapse'])

    def check_dead(self):
        return self.monitor.get_cords(self.resources['death_counter'], threshold=.8)

    def check_close_button(self):
        return self.monitor.get_cords(self.resources['yellow_close_button']) \
               or self.monitor.get_cords(self.resources['orange_close_button'])

    def find_event_reference(self):
        return self.monitor.get_cords(self.resources['event_reference'])

    def find_mail_icon(self):
        return self.monitor.get_cords(self.resources['mail_icon'])

    def find_monster_icon(self):
        return self.monitor.get_cords(self.resources['monster_icon'])
