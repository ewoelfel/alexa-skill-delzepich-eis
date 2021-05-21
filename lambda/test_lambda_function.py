import datetime
import requests
from unittest import TestCase, mock
from test_data import TestData
from lambda_function import get_icecreams_of_date


class TestGet_icecreams(TestCase):

    @mock.patch('requests.get')
    def test_get_icecreams_of_date(self, mock_get):
        # given
        requests.get.return_value = TestData.delzepich_html_get()

        # when
        date = datetime.datetime.strptime('2021-05-21', '%Y-%m-%d')
        variations = get_icecreams_of_date(date)

        # then
        assert variations == ['Franzbrötchen', 'Herrenschoki', 'Mascarpone - Waldfrucht', 'Sesam - Krokant', 'Schoko', 'Vanille', 'Cheesecake', 'Tagessorbet']