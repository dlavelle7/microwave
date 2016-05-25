import unittest
import microwave
from mock import Mock, patch


class TestMicrowave(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('microwave.FrameComponent', Mock())
    def test_(self):
        # TODO: Write UTs
        micro = microwave.Microwave(Mock())
        #import ipdb; ipdb.set_trace()
