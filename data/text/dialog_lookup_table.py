from functools import partial

from pygame import display, time, mixer

from src.common import play_sound, confirmation_sfx, special_item_sfx
from src.config import MUSIC_ENABLED, TILE_SIZE
from src.game_functions import draw_all_tiles_in_current_map
from src.menu_functions import draw_player_sprites, draw_character_sprites
from src.visual_effects import fade


class DialogLookup:
    def __init__(self, command_menu):
        self.command_menu = command_menu
        self.player = command_menu.player
        self.screen = command_menu.screen
        self.current_map = command_menu.current_map
        self.background = command_menu.background
        self.camera_position = command_menu.camera_position

        weapons_and_armor_intro = "We deal in weapons and armor.\n" \
                                  "Dost thou wish to buy anything today?"

        where_is_princess_gwaelin = "Where oh where can I find Princess Gwaelin?"
        welcome_to_tantegel = "Welcome to Tantegel Castle."
        brecconary_inn_cost = 6
        garinham_inn_cost = 25
        tools_intro = "Welcome.\n" \
                      "We deal in tools.\n" \
                      "What can I do for thee?"
        self.lookup_table = {
            'TantegelThroneRoom': {
                'KING_LORIK': {'dialog': (
                    "Descendant of Erdrick, listen now to my words.",
                    "It is told that in ages past Erdrick fought demons with a Ball of Light.",
                    "Then came the Dragonlord who stole the precious globe and hid it in the darkness.",
                    f"Now, {self.player.name}, thou must help us recover the Ball of Light and restore peace to our land.",
                    "The Dragonlord must be defeated.",
                    "Take now whatever thou may find in these Treasure Chests to aid thee in thy quest.",
                    "Then speak with the guards, for they have much knowledge that may aid thee.",
                    f"May the light shine upon thee, {self.player.name}."
                ), 'post_initial_dialog': "When thou art finished preparing for thy departure, please see me.\n"
                                          "I shall wait.",
                    'returned_dialog': (
                        f"I am greatly pleased that thou hast returned, {self.player.name}.",
                        f"Before reaching thy next level of experience thou must gain {self.player.points_to_next_level} Points.",
                        "Will thou tell me now of thy deeds so they won't be forgotten?",
                        # if yes:
                        "Thy deeds have been recorded on the Imperial Scrolls of Honor.",
                        "Dost thou wish to continue thy quest?",
                        # if yes:
                        f"Goodbye now, {self.player.name}.\n'Take care and tempt not the Fates.",
                        # if no:
                        # "Rest then for awhile."
                    )},
                'RIGHT_FACE_GUARD': {'dialog': (
                    "East of this castle is a town where armor, weapons, and many other items may be purchased.",
                    f"Return to the Inn for a rest if thou art wounded in battle, {self.player.name}.",
                    "Sleep heals all."
                )},
                'LEFT_FACE_GUARD': {'dialog': (
                    "If thou hast collected all the Treasure Chests, a key will be found.",
                    "Once used, the key will disappear, but the door will be open and thou may pass through."
                )},
                'ROAMING_GUARD': {'dialog': (
                    # know_about_princess = input("Dost thou know about Princess Gwaelin?'")
                    # if not know_about_princess:
                    #     print_with_beep_sfx("Half a year now hath passed since the Princess was kidnapped by the enemy.")
                    #     print_with_beep_sfx("Never does the King speak of it, but he must be suffering much.")
                    # else:
                    #     print_with_beep_sfx(f"{self.player.name}, please save the Princess.")
                    # TODO: Reset this later to use input(), but just for testing it out we can leave it this way for now.
                    "Dost thou know about Princess Gwaelin?",
                    "Half a year now hath passed since the Princess was kidnapped by the enemy.",
                    "Never does the King speak of it, but he must be suffering much."
                )}},
            'TantegelCourtyard': {
                'MERCHANT': {'dialog': ("Magic keys! They will unlock any door. \nDost thou wish to purchase one for 85 GOLD?",)},
                'MERCHANT_2': {'dialog': "We are merchants who have traveled much in this land. "
                                         "Many of our colleagues have been killed by servants of the Dragonlord."},
                'MERCHANT_3': {'dialog': "Rumor has it that entire towns have been destroyed by the Dragonlord's servants."},
                'MAN': {'dialog': "To become strong enough to face future trials thou must first battle many foes."},
                'MAN_2': {'dialog': "There was a time when Brecconary was a paradise.\n"
                                    "Then the Dragonlord's minions came."},
                'WOMAN': {'dialog': ("When the sun and rain meet, a Rainbow Bridge shall appear.", "It's a legend.")},
                'WOMAN_2': {'dialog': where_is_princess_gwaelin},
                'RIGHT_FACE_GUARD': {'dialog': where_is_princess_gwaelin},
                'LEFT_FACE_GUARD': {'dialog': welcome_to_tantegel},
                'DOWN_FACE_GUARD': {'dialog': (
                    "King Lorik will record thy deeds in his Imperial Scroll so thou may return to thy quest later.",)},
                'UP_FACE_GUARD': {'dialog': "If thou art planning to take a rest, first see King Lorik."},
                'RIGHT_FACE_GUARD_2': {'dialog': welcome_to_tantegel},
                'WISE_MAN': {'dialog': f"{self.player.name}'s coming was foretold by legend. "
                                       f"May the light shine upon this brave warrior.", 'side_effects': (self.player.restore_mp,)}},
            'TantegelCellar': {'WISE_MAN': {'dialog': ("I have been waiting long for one such as thee.", "Take the Treasure Chest.")}},
            'Brecconary': {
                'MAN': {'dialog': "There is a town where magic keys can be purchased."},
                'WISE_MAN': {'dialog': "If thou art cursed, come again."},
                'MERCHANT': {'dialog': (weapons_and_armor_intro,)},
                'MERCHANT_2': {'dialog': [self.get_inn_intro(brecconary_inn_cost),
                                          partial(play_sound, confirmation_sfx),
                                          # prompt yes or no

                                          # if yes:

                                          # if has enough money:
                                          "Good night.",
                                          partial(self.inn_sleep, brecconary_inn_cost),
                                          "Good morning.\n"
                                          "Thou seems to have spent a good night.",
                                          "I shall see thee again."

                                          # else (not enough money):
                                          # "Thou hast not enough money.",

                                          # if no
                                          # "Okay.\n"
                                          # "Good-bye, traveler."
                                          ]},
                'WOMAN_2': {'dialog': "Welcome! \n"
                                      "Enter the shop and speak to its keeper across the desk."},
            },
            'Garinham': {
                'MERCHANT': {'dialog': (tools_intro,)},
                'MERCHANT_2': {'dialog': (
                    self.get_inn_intro(garinham_inn_cost),
                )},
                'MERCHANT_3': {'dialog': weapons_and_armor_intro},
                'WISE_MAN': {'dialog': "Many believe that Princess Gwaelin is hidden away in a cave."}

            }
        }

        for map_dict in self.lookup_table.values():
            for character_identifier, character_dict in map_dict.items():
                character_dict['dialog_character'] = character_identifier

    @staticmethod
    def get_inn_intro(inn_cost):
        return "Welcome to the traveler's Inn.\n" \
               f"Room and board is {inn_cost} GOLD per night.\n" \
               "Dost thou want a room?"

    def inn_sleep(self, inn_cost):
        fade(fade_out=True, screen=self.screen)
        if MUSIC_ENABLED:
            mixer.music.stop()
        play_sound(special_item_sfx)
        self.player.restore_hp()
        self.player.restore_mp()
        self.player.gold -= inn_cost
        time.wait(3000)
        if MUSIC_ENABLED:
            mixer.music.load(self.current_map.music_file_path)
            mixer.music.play(-1)
        draw_all_tiles_in_current_map(self.current_map, self.background)
        draw_player_sprites(self.current_map, self.background, self.player.column, self.player.row)
        for character, character_dict in self.current_map.characters.items():
            if character != 'HERO':
                draw_character_sprites(self.current_map, self.background, character_dict['coordinates'][1], character_dict['coordinates'][0], character)
        self.screen.blit(self.background, self.camera_position)
        self.screen.blit(self.command_menu.command_menu_surface, (TILE_SIZE * 5, TILE_SIZE * 1))
        display.flip()
