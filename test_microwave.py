import unittest
import microwave
from mock import Mock, patch

class MockWidget:
    """Old style class to mock base class Tkinter widgets."""

    def __init__(self, *args, **kwargs):
        self.master = args[0]

    def __setitem__(self, name, value):
        pass

    def grid(self, *args, **kwargs):
        pass

    def pack(self, *args, **kwargs):
        pass

    def next(self):
        return Mock()


class TestMicrowave(unittest.TestCase):

    def setUp(self):
        microwave.threading = Mock()
        microwave.time = Mock()

    def tearDown(self):
        pass

    @patch('microwave.Frame', MockWidget)
    @patch('microwave.Label', MockWidget)
    @patch('microwave.Button', MockWidget)
    def test_states(self):
        # Mock Tkinter.Frame & Tkinter.Button base classes
        microwave.FrameComponent.__bases__ = (MockWidget,)
        microwave.NumPadButton.__bases__ = (MockWidget,)
        # Create microwave instance
        micro = microwave.Microwave(Mock())
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))
        self.assertEquals(0, micro.timer.secs)
        # Stopped -> stop() = Stopped & resets secs
        micro.timer.secs = 2
        micro.state.stop()
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))
        self.assertEquals(0, micro.timer.secs)
        # Stopped -> start() & no secs = Stopped
        micro.state.start()
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))
        # Stopped -> start() with secs = Cooking
        micro.timer.secs = 2
        micro.state.start()
        self.assertTrue(isinstance(micro.state, microwave.CookingState))
        # TODO: Cooking -> start() = Cooking
        micro.set_state(microwave.CookingState(micro))
        micro.state.start()
        self.assertTrue(isinstance(micro.state, microwave.CookingState))
        # TODO: Cooking -> stop() = Stoped
        micro.set_state(microwave.CookingState(micro))
        micro.state.stop()
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))

    def test_countdown(self):
        # TODO
        pass
