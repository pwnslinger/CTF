import requests


HUMAN_COOKIE = "hq6fc0d7e7siehrr495k0c12v0"

ALIEN_COOKIE = "al5ohnrlrc7b8n24mj7f8q9550"



def human_post(content, msg_type="human", cookie=HUMAN_COOKIE):
    return requests.post("http://138.68.228.12/omega_sector.php",

                         data={"message": content, "type": msg_type},

                         cookies={"PHPSESSID": cookie})



def alien_post(content, msg_type="alien", cookie=ALIEN_COOKIE):
    return requests.post("http://138.68.228.12/alien_sector.php",

                         data={"message": content, "type": msg_type},

                         cookies={"PHPSESSID": cookie})



def check_valid(content):

    if "Uh huh? Wut is this language?" in content:

        # Invalid character (sent by both modes)

        return False

    if "Too long, we can only receive 40 letters for each message" in content:

        # Too long (sent by human mode)

        return False

    if "Signal OVERLOAD!!!!! only 40 o e i e" in content:

        # Too long (sent by alien mode)

        return False

    if not "Saved in " in content:

        # Catch all

        return False

    return True



def grab_url_from_content(content):

    if not check_valid(content):

        raise StandardError("Content was invalid")

    start = "Saved in "

    end = "</h2>"

    start_idx = content.index(start) + len(start)

    part1 = content[start_idx:]

    return part1[:part1.index(end)]



def get_result(content):

    path = grab_url_from_content(content)

    return requests.get("http://138.68.228.12/" + path)



def is_human_string_valid(data):

    return check_valid(human_post(data).content)



def is_alien_string_valid(data):

    return check_valid(alien_post(data).content)



def get_allowed():

    human_allowed = set()

    alien_allowed = set()

    for i in xrange(256):

        c = chr(i)

        if is_human_string_valid(c):

            human_allowed.add(c)

        if is_alien_string_valid(c):

            alien_allowed.add(c)

    return human_allowed, alien_allowed
