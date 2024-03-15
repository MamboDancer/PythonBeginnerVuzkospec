import requests


class Leaderboard:
    lb_url = None

    def __init__(self, url):
        self.lb_url = url

    def get_scores(self):
        scores_json = requests.get(self.lb_url + "/json").json()
        try:
            scores_json = scores_json["dreamlo"]["leaderboard"]["entry"]
        except TypeError:
            return [{"name": "Scoreboard", "score": "Empty"}]
        return [scores_json] if type(scores_json) is not list else scores_json

    def get_wins(self, username):
        for score in self.get_scores():
            if score["name"] == username:
                return score["score"]
        return 0

    def update_leaderboard(self, username):
        user_wins = int(self.get_wins(username))
        requests.request("POST", self.lb_url + f"/add/{username}/{user_wins + 1}")
