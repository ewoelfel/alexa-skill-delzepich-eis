class TestData():

    def delzepich_html_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, text, status_code):
                self.text = text
                self.status_code = status_code

            def text(self):
                return self.text

        with open('test_output.html', 'r') as file:
            data = file.read().replace('\n', '')

        return MockResponse(data, 200)
