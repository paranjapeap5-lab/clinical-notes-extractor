class FakeClient:
    """Stand-in for Claude. Returns canned text so we can build and test
    the whole pipeline with no API cost and identical output every run."""

    def __init__(self, canned_response: str):
        self.canned_response = canned_response

    def complete(self, prompt: str) -> str:
        return self.canned_response
