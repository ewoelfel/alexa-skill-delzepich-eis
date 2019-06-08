import datetime
import requests
from unittest import TestCase, mock
from test_data import TestData
from lambda_function import get_icecreams_of_date


class TestGet_icecreams(TestCase):

    @mock.patch('requests.get')
    def test_get_icecreams_of_date(self, mock_getr):
        # given
        requests.get.return_value = TestData.delzepich_html_get()

        # when
        date = datetime.datetime.strptime('2019-06-08', '%Y-%m-%d')
        types = get_icecreams_of_date(date)

        # then
        assert types == ['Schoko','Himbeer - Baiser', 'Schokokuchen', 'Mokka',
                         'Vanille', 'Mascarpone - Blaubeer', 'Milkyway',
                         'Tagessorbet (laktosefrei)']
