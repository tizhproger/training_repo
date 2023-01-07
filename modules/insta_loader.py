import re
import instaloader
import os.path

from instaloader import Profile
from instaloader.exceptions import ProfileNotExistsException


class Instload():
    def __init__(self):
        L = instaloader.Instaloader()
        #L.login("look.atme42", "Lookatme42")
        #L.load_session_from_file("look.atme42_sesssion")
        self.L = L
    
    
    def download_story(self, link) -> dict:
        tries = 0
        quantity = 0
        res = re.search("(?:https?:\/\/)?(?:www.)?instagram.com\/?([a-zA-Z0-9\.\_\-]+)?\/([p]+)?([reel]+)?([tv]+)?([stories]+)?\/([a-zA-Z0-9\-\_\.]+)\/?([0-9]+)?", link)
        if type(res) is re.Match:
            if res.group(5) == 'stories':
                #user_id = Profile.from_username(self.L.context, res.group(6)).userid
                user_id = self.L.check_profile_id(res.group(6)).userid
                if user_id is None:
                    return {'error': 'User not found'}

                for story in self.L.get_stories(userids=[user_id]):
                    for item in story.get_items():
                        quantity += 1 
                        if str(item.mediaid) == res.group(7):
                            if item.is_video:
                                return {'video': item.video_url}
                            else:
                                return {'photo': item.url}
                        else:
                            tries += 1
                if tries == quantity:
                    return {'error': 'Story not found'}
            else:
                return {'error': 'It is not a story link'}


    def all_stories(self, username) -> dict:
        links = []
        try:
            #user_id = Profile.from_username(self.L.context, res.group(6)).userid
            user_id = self.L.check_profile_id(username).userid
        except ProfileNotExistsException:
            user_id = None

        if user_id is None:
            return {'error': 'User not found'}

        for story in self.L.get_stories(userids=[user_id]):
            for item in story.get_items():
                if item.is_video:
                    links.append(item.video_url)
                else:
                    links.append(item.url)
        if len(links) == 0:
            return {'error': 'Stories not found'}
        links.reverse()
        return links
