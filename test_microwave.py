import unittest
import microwave
from mock import Mock, patch

class MyMock:
    """Old style class to mock base class Frame."""

    def __setitem__(self, name, value):
        pass

    def grid(self, row, column):
        pass

    def pack(self):
        pass

    def next(self):
        return Mock()


class MockComponent(dict):
    """Subclass dict for item assignment and have a pack() function."""

    def pack(self):
        pass


class TestMicrowave(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('microwave.Frame', Mock())
    @patch('microwave.Label', Mock(return_value=MockComponent()))
    @patch('microwave.Button', Mock())
    def test_states(self):
        # Mock Tkinter.Frame & Tkinter.Button base classes
        microwave.FrameComponent.__bases__ = (MyMock,)
        microwave.NumPadButton.__bases__ = (MyMock,)
        # Create microwave instance
        micro = microwave.Microwave(Mock())
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))
        self.assertEquals(0, micro.timer.secs)
        # Stopped -> Stopped = Stopped
        micro.state.stop()
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))
        # Stopped -> Cooking no secs = Stopped
        micro.state.start()
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))
        # Stopped -> Cooking with secs = Cooking
        #micro.timer.secs = 2
        #micro.state.start()
        #self.assertTrue(isinstance(micro.state, microwave.CookingState))
