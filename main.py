import cv2
import time
from monitor import Monitor
from winapi import WinApi
from detection import Detection


def debug_screen():
    while True:
        monitor.show()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        monitor.update()
        time.sleep(1 / 60)


def reset_screen():
    close_button = detection.check_close_button()
    afk = detection.check_afk()
    back_button = detection.check_back_button()
    chat_open = detection.check_chat()
    if close_button:
        winapi.mouse_click(close_button[0])
    if afk:
        winapi.mouse_click(afk[0])
    if back_button:
        winapi.mouse_click(back_button[0])
    if chat_open:
        winapi.mouse_click(chat_open[0])


def enable_battle():
    battle = detection.check_battle()
    if battle[0] is False:
        winapi.mouse_click(battle[1][0])


def click_map():
    event_ref = detection.find_event_reference()
    if event_ref:
        map_coords = event_ref[0][0] + 70, event_ref[0][1]
        winapi.mouse_click(map_coords)


# title of the nox window
window_title = 'main'
# we scale images to this size, to keep it consistent
scaled_resolution = [502, 892]
# the index on the list of the monster you want to hunt
monster_to_hunt_index = 0
# might need tweaking, depending on the resolution
monster_list_item_height = 30
# jump spawns, useful when you cant kill someone that is in your spawn
jump_spawns = True
# how much time does it wait, before looping again (seconds)
screenshot_delay = 2

winapi = WinApi(window_title, scaled_resolution)
handle = winapi.get_handle()

if handle:
    monitor = Monitor(handle, True, scaled_resolution)
    detection = Detection(monitor)
    while True:
        monitor.update()
        reset_screen()
        enable_battle()
        is_dead = detection.check_dead()
        is_afk = detection.check_afk()
        if is_dead or is_afk:
            if is_afk:
                winapi.mouse_click(is_afk[0])
                time.sleep(1)
            elif is_dead:
                time.sleep(10)
            monitor.update()
            # go to hunt again
            click_map()
            time.sleep(2)
            monitor.update()
            monster_icon = detection.find_monster_icon()
            if monster_icon:
                monster_position = monster_icon[0][0], monster_icon[0][1] + \
                                   (monster_to_hunt_index + 1) * monster_list_item_height
                # this will change the spawn you will try to go, maybe the next one is safer
                if jump_spawns:
                    monster_to_hunt_index += 1
                    # the list only shows 9 monsters, most maps have less than that, but we could scroll later
                    if monster_to_hunt_index >= 9:
                        monster_to_hunt_index = 0
                winapi.mouse_click(monster_position)
        time.sleep(screenshot_delay)
else:
    print('handle not found, check the window title or open your emulator.')
