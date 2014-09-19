import unittest
import vimwiki2markdown as sut


@unittest.skip("Don't forget to test!")
class Vimwiki2MarkdownTests(unittest.TestCase):

    def test_example_fail(self):
        result = sut.vimwiki2markdown_example()
        self.assertEqual("Happy Hacking", result)
