import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime, timedelta, date
from wled_fcsp_controller.Score import Score

class SpiegelCrawler:
    def __init__(self):
        self.endpoint = "https://sportdaten.spiegel.de"
        self.team_name = 'pauli'

    def next_pauli_match(self):
        for i in range(14):
            date_obj = (datetime.today() + timedelta(days=i)).date()
            endpoint = self.endpoint + f'/dn{str(date_obj)}'
            req = requests.get(endpoint)
            soup = BeautifulSoup(req.text, features="html.parser")

            match_results = soup.find_all("div", {'class': "match-result match-result-0"})
            match_results = [x.contents[0] for x in match_results if isinstance(x.contents[0], Tag) and (self._filter_fcsp_upcoming_matches(x.contents[0]) or self._filter_fcsp_live_matches(x.contents[0]))]

            if len(match_results) > 0:
                return self._start_time_to_datetime(match_results[0].parent.previous, date_obj)
        return None

    def get_current_fcsp_score(self):
        req = requests.get(self.endpoint)
        soup = BeautifulSoup(req.text, features="html.parser")

        match_results = soup.find_all("div", {'class': "match-result match-result-0"})
        match_results = [x.contents[0] for x in match_results if isinstance(x.contents[0], Tag) and (self._filter_fcsp_live_matches(x.contents[0]) or self._filter_fcsp_upcoming_matches(x.contents[0]))]
        if len(match_results) > 0:
            match_result = match_results[0]

            score = self.tag2score(match_result)
            return score
        return None

    @staticmethod
    def _start_time_to_datetime(start_time: str, date_obj: date):
        date_obj = date_obj.strftime('%Y-%m-%d')
        match_start_time = datetime.strptime(f'{date_obj}_{start_time}', '%Y-%m-%d_%H:%M')
        return match_start_time

    def _filter_fcsp_live_matches(self, match_result: Tag):
        is_fcsp_live = match_result.has_attr('href') and 'liveticker' in match_result.attrs['href'] and self.team_name in match_result.attrs['href']
        return is_fcsp_live

    def _filter_fcsp_upcoming_matches(self, match_result: Tag):
        is_fcsp = match_result.has_attr('href') and 'bilanz' in match_result.attrs['href'] and self.team_name in match_result.attrs['href']
        return is_fcsp

    def _parse_score_str_and_teams(self, score: str, teams: str) -> Score:
        score = score.replace(' ', '')
        score = (score.split(':')[0], score.split(':')[1])
        score = (int(score[0]), int(score[1])) if score != ('-', '-') else (0, 0)

        home, away = teams.split('_')
        is_home_game = self.team_name in home
        return Score(*score) if is_home_game else Score(*(score[1], score[0]))

    def tag2score(self, match_result: Tag) -> Score:
        assert 'href' in match_result.attrs

        req = requests.get(f'{self.endpoint}{match_result.attrs["href"]}')
        soup = BeautifulSoup(req.text, features="html.parser")
        score_tag = soup.findAll("div", {'class': "match-result match-result-0"})[0]
        score_str = score_tag.string
        teams = match_result.attrs['href'].split('/')[-3]
        return self._parse_score_str_and_teams(score_str, teams)


if __name__ == '__main__':
    c = SpiegelCrawler()
    print(c.get_current_fcsp_score())


