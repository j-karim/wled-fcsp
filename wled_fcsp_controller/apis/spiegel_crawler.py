import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime, timedelta, date
from wled_fcsp_controller.Score import Score

class SpiegelCrawler:
    def __init__(self):
        self.endpoint = "https://sportdaten.spiegel.de"

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

            score = self._tag_to_score(match_result)
            return score
        return None

    @staticmethod
    def _start_time_to_datetime(start_time: str, date_obj: date):
        date_obj = date_obj.strftime('%Y-%m-%d')
        match_start_time = datetime.strptime(f'{date_obj}_{start_time}', '%Y-%m-%d_%H:%M')
        return match_start_time

    @staticmethod
    def _filter_fcsp_live_matches(match_result: Tag):

        is_fcsp_live = match_result.has_attr('href') and 'liveticker' in match_result.attrs['href'] and 'pauli' in match_result.attrs['href']
        return is_fcsp_live

    @staticmethod
    def _filter_fcsp_upcoming_matches(match_result: Tag):
        is_fcsp_live = match_result.has_attr('href') and 'bilanz' in match_result.attrs['href'] and 'pauli' in match_result.attrs['href']
        return is_fcsp_live

    @staticmethod
    def _tag_to_score(match_result: Tag):
        score = match_result.string

        score = (score.split(':')[0], score.split(':')[1])
        score = (int(score[0]), int(score[1])) if score != ('-', '-') else (0, 0)

        assert match_result.has_attr('href') and ('liveticker' in match_result.attrs['href'] or 'bilanz' in match_result.attrs['href'])
        link = match_result.attrs['href']
        match = link.split('/')[-3]
        home, away = match.split('_')
        is_home_game = 'pauli' in home
        return Score(*score) if is_home_game else Score(*(score[1], score[0]))


if __name__ == '__main__':
    c = SpiegelCrawler()
    print(c.get_current_fcsp_score())


