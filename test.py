import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from rky.brain import RockyBrain, HYDRATION

class TestRockyBrain(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        self.test_file = self.test_dir / "test_state.json"
        
        self.patcher_dir = patch('rky.brain._STATE_DIR', self.test_dir)
        self.patcher_file = patch('rky.brain._STATE_FILE', self.test_file)
        self.patcher_dir.start()
        self.patcher_file.start()
        
        self.brain = RockyBrain()

    def tearDown(self):
        self.patcher_dir.stop()
        self.patcher_file.stop()
        self.temp_dir.cleanup()

    def test_initialization(self):
        state = self.brain.get_state()
        self.assertEqual(state["hydration"], 0.6)
        self.assertEqual(state["focus"], 0.5)
        self.assertEqual(self.brain._tick, 0)

    def test_apply_control_distraction(self):
        initial_focus = self.brain.get_state()["focus"]
        initial_distraction = self.brain.get_state()["distraction"]
        
        self.brain.process_input("youtube")
        new_state = self.brain.get_state()
        
        self.assertLess(new_state["focus"], initial_focus)
        self.assertGreater(new_state["distraction"], initial_distraction)

    def test_hydration_logging(self):
        self.brain._psi[HYDRATION] = 0.2
        self.brain.log_drink()
        self.assertGreater(self.brain.get_state()["hydration"], 0.2)

    def test_quest_persistence(self):
        self.brain.add_quest("4821", {"name": "Test MatrixMind", "complete": False})
        
        del self.brain
        rebooted_brain = RockyBrain()
        
        quests = rebooted_brain.get_all_quests()
        self.assertEqual(len(quests), 1)
        self.assertEqual(quests[0]["id"], "4821")
        self.assertFalse(quests[0]["complete"])

    def test_quest_completion_momentum(self):
        self.brain.add_quest("9999", {"name": "Test Completion", "complete": False})
        initial_momentum = self.brain.get_state()["momentum"]
        
        success = self.brain.complete_quest("9999")
        
        self.assertTrue(success)
        self.assertEqual(len(self.brain.get_active_quests()), 0)
        self.assertGreater(self.brain.get_state()["momentum"], initial_momentum)

if __name__ == '__main__':
    unittest.main()