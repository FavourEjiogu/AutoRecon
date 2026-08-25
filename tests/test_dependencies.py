import unittest
from unittest.mock import patch
from autorecon.core.dependencies import check_tool, check_all_dependencies, get_install_command
from autorecon.core.config import TOOLS

class TestDependencies(unittest.TestCase):
    @patch('shutil.which')
    def test_check_tool_exists(self, mock_which):
        mock_which.return_value = "/usr/bin/ping"
        self.assertTrue(check_tool("ping"))
        
    @patch('shutil.which')
    def test_check_tool_missing(self, mock_which):
        mock_which.return_value = None
        self.assertFalse(check_tool("missingtool"))

    @patch('shutil.which')
    def test_check_all_dependencies(self, mock_which):
        # Simulate 'ping' and 'whois' exist, others do not
        def side_effect(arg):
            if arg in ["ping", "whois"]:
                return f"/usr/bin/{arg}"
            return None
        mock_which.side_effect = side_effect
        
        status, missing = check_all_dependencies()
        self.assertTrue(status["ping"])
        self.assertTrue(status["whois"])
        self.assertFalse(status["nmap"])
        self.assertIn("nmap", missing)
        self.assertIn("nikto", missing)
        
    def test_get_install_command(self):
        missing = ["nmap", "nikto"]
        cmd = get_install_command(missing)
        self.assertIn("apt-get install", cmd)
        self.assertIn(TOOLS["nmap"], cmd)
        self.assertIn(TOOLS["nikto"], cmd)

if __name__ == '__main__':
    unittest.main()
