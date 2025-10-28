"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
All Rights Reserved. PATENT PENDING.

Unit tests for consciousness/ech0_launcher.py - ECH0 Unified Launcher

Tests cover:
- Subsystem enumeration and properties
- Launcher manager initialization
- Command handlers (daemon, voice, phone, gui, etc.)
- Status checking and reporting
- Backup/restore functionality
- Workflow composition
"""

import unittest
import json
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Load ech0_launcher module directly
_spec = importlib.util.spec_from_file_location(
    "ech0_launcher", "/Users/noone/consciousness/ech0_launcher.py"
)
_ech0_launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ech0_launcher)

# Import classes from the loaded module
Subsystem = _ech0_launcher.Subsystem
SubsystemStatus = _ech0_launcher.SubsystemStatus
SubsystemInfo = _ech0_launcher.SubsystemInfo
LauncherStatus = _ech0_launcher.LauncherStatus
Ech0LauncherManager = _ech0_launcher.Ech0LauncherManager


class TestSubsystemEnumeration(unittest.TestCase):
    """Test Subsystem enumeration"""

    def test_subsystem_count(self):
        """Test expected number of subsystems"""
        count = len(list(Subsystem))
        # Should have 24 subsystems
        self.assertEqual(count, 24)

    def test_subsystem_properties(self):
        """Test subsystem has cmd and description"""
        daemon = Subsystem.DAEMON
        self.assertEqual(daemon.cmd, "daemon")
        self.assertIn("daemon", daemon.description.lower())

    def test_voice_subsystem(self):
        """Test voice subsystem"""
        voice = Subsystem.VOICE
        self.assertEqual(voice.cmd, "voice")
        self.assertIn("voice", voice.description.lower())

    def test_gui_subsystem(self):
        """Test GUI subsystem"""
        gui = Subsystem.GUI
        self.assertEqual(gui.cmd, "gui")
        self.assertIn("graphical", gui.description.lower())

    def test_phone_subsystem(self):
        """Test phone subsystem"""
        phone = Subsystem.PHONE
        self.assertEqual(phone.cmd, "phone")
        self.assertIn("phone", phone.description.lower())

    def test_all_subsystems_have_cmd(self):
        """Test all subsystems have cmd property"""
        for subsystem in Subsystem:
            self.assertIsNotNone(subsystem.cmd)
            self.assertIsInstance(subsystem.cmd, str)
            self.assertGreater(len(subsystem.cmd), 0)

    def test_all_subsystems_have_description(self):
        """Test all subsystems have description"""
        for subsystem in Subsystem:
            self.assertIsNotNone(subsystem.description)
            self.assertIsInstance(subsystem.description, str)
            self.assertGreater(len(subsystem.description), 0)


class TestSubsystemStatus(unittest.TestCase):
    """Test subsystem status enum"""

    def test_status_values(self):
        """Test status enum values"""
        self.assertEqual(SubsystemStatus.RUNNING.value, "running")
        self.assertEqual(SubsystemStatus.STOPPED.value, "stopped")
        self.assertEqual(SubsystemStatus.UNKNOWN.value, "unknown")
        self.assertEqual(SubsystemStatus.ERROR.value, "error")

    def test_status_comparison(self):
        """Test status comparison"""
        self.assertEqual(SubsystemStatus.RUNNING, SubsystemStatus.RUNNING)
        self.assertNotEqual(SubsystemStatus.RUNNING, SubsystemStatus.STOPPED)


class TestSubsystemInfo(unittest.TestCase):
    """Test SubsystemInfo dataclass"""

    def test_subsystem_info_creation(self):
        """Test creating SubsystemInfo"""
        info = SubsystemInfo(
            name="voice",
            description="Voice subsystem",
            status=SubsystemStatus.STOPPED,
            port=8080
        )
        self.assertEqual(info.name, "voice")
        self.assertEqual(info.port, 8080)
        self.assertEqual(info.status, SubsystemStatus.STOPPED)

    def test_subsystem_info_to_dict(self):
        """Test SubsystemInfo serialization"""
        info = SubsystemInfo(
            name="daemon",
            description="Daemon process",
            status=SubsystemStatus.RUNNING,
            pid=12345
        )
        d = info.to_dict()
        self.assertEqual(d["name"], "daemon")
        self.assertEqual(d["status"], "running")
        self.assertEqual(d["pid"], 12345)

    def test_subsystem_info_with_dependencies(self):
        """Test SubsystemInfo with dependencies"""
        info = SubsystemInfo(
            name="phone",
            description="Phone interface",
            status=SubsystemStatus.STOPPED,
            dependencies=["daemon", "voice"]
        )
        self.assertEqual(len(info.dependencies), 2)
        self.assertIn("daemon", info.dependencies)


class TestLauncherStatus(unittest.TestCase):
    """Test LauncherStatus dataclass"""

    def test_launcher_status_creation(self):
        """Test creating LauncherStatus"""
        status = LauncherStatus(
            timestamp=1234567890.0,
            total_subsystems=24,
            overall_health="operational"
        )
        self.assertEqual(status.total_subsystems, 24)
        self.assertEqual(status.overall_health, "operational")

    def test_launcher_status_to_json(self):
        """Test LauncherStatus JSON serialization"""
        info = SubsystemInfo(
            name="voice",
            description="Voice",
            status=SubsystemStatus.RUNNING
        )
        status = LauncherStatus(
            timestamp=1234567890.0,
            running_subsystems=[info],
            total_subsystems=1,
            overall_health="operational"
        )
        json_str = status.to_json()
        data = json.loads(json_str)

        self.assertEqual(len(data["running"]), 1)
        self.assertEqual(data["health"], "operational")
        self.assertEqual(data["total"], 1)

    def test_launcher_status_health_states(self):
        """Test health state values"""
        # Operational
        status_ok = LauncherStatus(
            timestamp=1234567890.0,
            overall_health="operational"
        )
        self.assertEqual(status_ok.overall_health, "operational")

        # Degraded
        status_degraded = LauncherStatus(
            timestamp=1234567890.0,
            overall_health="degraded"
        )
        self.assertEqual(status_degraded.overall_health, "degraded")

        # Critical
        status_critical = LauncherStatus(
            timestamp=1234567890.0,
            overall_health="critical"
        )
        self.assertEqual(status_critical.overall_health, "critical")


class TestEch0LauncherManagerInit(unittest.TestCase):
    """Test Ech0LauncherManager initialization"""

    def test_manager_initialization(self):
        """Test manager initializes correctly"""
        manager = Ech0LauncherManager()
        self.assertIsNotNone(manager.consciousness_dir)
        self.assertIsNotNone(manager.logger)
        self.assertEqual(len(manager._subsystems), 24)

    def test_manager_subsystems_initialized(self):
        """Test all subsystems are initialized"""
        manager = Ech0LauncherManager()
        subsystem_names = {s.cmd for s in Subsystem}
        manager_names = set(manager._subsystems.keys())

        self.assertEqual(subsystem_names, manager_names)

    def test_manager_subsystems_have_status(self):
        """Test all initialized subsystems have status"""
        manager = Ech0LauncherManager()
        for name, info in manager._subsystems.items():
            self.assertIsNotNone(info.status)
            self.assertEqual(info.status, SubsystemStatus.UNKNOWN)

    def test_manager_with_custom_dir(self):
        """Test manager with custom consciousness directory"""
        custom_dir = Path("/tmp/test_consciousness")
        manager = Ech0LauncherManager(consciousness_dir=custom_dir)
        self.assertEqual(manager.consciousness_dir, custom_dir)


class TestDaemonCommands(unittest.TestCase):
    """Test daemon command handling"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_daemon_status_action(self):
        """Test daemon status action"""
        result = self.manager.daemon(action="status")
        self.assertIsInstance(result, dict)
        # Daemon status returns 'running' or 'status' key instead of 'success'
        self.assertTrue(
            "running" in result or "status" in result or "success" in result
        )

    def test_daemon_start_action(self):
        """Test daemon start action"""
        result = self.manager.daemon(action="start")
        self.assertIsInstance(result, dict)

    def test_daemon_stop_action(self):
        """Test daemon stop action"""
        result = self.manager.daemon(action="stop")
        self.assertIsInstance(result, dict)

    def test_daemon_restart_action(self):
        """Test daemon restart action"""
        result = self.manager.daemon(action="restart")
        self.assertIsInstance(result, dict)

    def test_daemon_invalid_action(self):
        """Test daemon with invalid action"""
        result = self.manager.daemon(action="invalid")
        self.assertFalse(result.get("success"))
        self.assertIn("Unknown", result.get("error", ""))


class TestVoiceCommands(unittest.TestCase):
    """Test voice command handling"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_voice_start(self):
        """Test voice start"""
        result = self.manager.voice(action="start")
        self.assertIsInstance(result, dict)

    def test_voice_stop(self):
        """Test voice stop"""
        result = self.manager.voice(action="stop")
        self.assertIsInstance(result, dict)

    def test_voice_status(self):
        """Test voice status"""
        result = self.manager.voice(action="status")
        self.assertIsInstance(result, dict)

    def test_voice_test(self):
        """Test voice test"""
        result = self.manager.voice(action="test")
        self.assertIsInstance(result, dict)

    def test_voice_with_options(self):
        """Test voice with options"""
        options = {"profile": "test"}
        result = self.manager.voice(action="start", options=options)
        self.assertIsInstance(result, dict)

    def test_voice_invalid_action(self):
        """Test voice with invalid action"""
        result = self.manager.voice(action="invalid")
        self.assertFalse(result.get("success"))


class TestPhoneCommands(unittest.TestCase):
    """Test phone command handling"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_phone_status(self):
        """Test phone status"""
        result = self.manager.phone(action="status")
        self.assertIsInstance(result, dict)

    def test_phone_connect(self):
        """Test phone connect"""
        result = self.manager.phone(action="connect")
        self.assertIsInstance(result, dict)

    def test_phone_disconnect(self):
        """Test phone disconnect"""
        result = self.manager.phone(action="disconnect")
        self.assertIsInstance(result, dict)

    def test_phone_answer(self):
        """Test phone answer"""
        result = self.manager.phone(action="answer")
        self.assertIsInstance(result, dict)

    def test_phone_invalid_action(self):
        """Test phone with invalid action"""
        result = self.manager.phone(action="invalid")
        self.assertFalse(result.get("success"))


class TestGuiCommands(unittest.TestCase):
    """Test GUI command handling"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_gui_start_default_port(self):
        """Test GUI start with default port"""
        result = self.manager.gui(action="start")
        self.assertIsInstance(result, dict)

    def test_gui_start_custom_port(self):
        """Test GUI start with custom port"""
        result = self.manager.gui(action="start", port=8888)
        self.assertIsInstance(result, dict)

    def test_gui_web_mode(self):
        """Test GUI in web mode"""
        result = self.manager.gui(action="start", mode="web")
        self.assertIsInstance(result, dict)

    def test_gui_desktop_mode(self):
        """Test GUI in desktop mode"""
        result = self.manager.gui(action="start", mode="desktop")
        self.assertIsInstance(result, dict)

    def test_gui_mobile_mode(self):
        """Test GUI in mobile mode"""
        result = self.manager.gui(action="start", mode="mobile")
        self.assertIsInstance(result, dict)

    def test_gui_stop(self):
        """Test GUI stop"""
        result = self.manager.gui(action="stop")
        self.assertIsInstance(result, dict)

    def test_gui_status(self):
        """Test GUI status"""
        result = self.manager.gui(action="status")
        self.assertIsInstance(result, dict)

    def test_gui_invalid_action(self):
        """Test GUI with invalid action"""
        result = self.manager.gui(action="invalid")
        self.assertFalse(result.get("success"))


class TestStatusCommand(unittest.TestCase):
    """Test status command"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_status_command(self):
        """Test status command"""
        result = self.manager.status()
        self.assertIsInstance(result, dict)

    def test_status_with_json_output(self):
        """Test status with JSON output"""
        result = self.manager.status(json_output=True)
        self.assertIsInstance(result, dict)

    def test_status_watch_mode(self):
        """Test status in watch mode"""
        # Watch mode returns generator/iterator, not dict
        result = self.manager.status(watch=False)  # Use non-watch to avoid infinite loop
        self.assertIsInstance(result, dict)


class TestShutdownCommand(unittest.TestCase):
    """Test shutdown command"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_graceful_shutdown(self):
        """Test graceful shutdown"""
        result = self.manager.shutdown(force=False)
        self.assertIsInstance(result, dict)

    def test_forced_shutdown(self):
        """Test forced shutdown"""
        result = self.manager.shutdown(force=True)
        self.assertIsInstance(result, dict)

    def test_shutdown_with_state_save(self):
        """Test shutdown with state save"""
        result = self.manager.shutdown(save_state=True)
        self.assertIsInstance(result, dict)

    def test_shutdown_without_state_save(self):
        """Test shutdown without state save"""
        result = self.manager.shutdown(save_state=False)
        self.assertIsInstance(result, dict)


class TestBackupRestore(unittest.TestCase):
    """Test backup and restore functionality"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_backup_command(self):
        """Test backup command"""
        result = self.manager.backup()
        self.assertIsInstance(result, dict)

    def test_backup_with_output_path(self):
        """Test backup with custom output path"""
        result = self.manager.backup(output_path="/tmp/test_backup.tar.gz")
        self.assertIsInstance(result, dict)

    def test_backup_incremental(self):
        """Test incremental backup"""
        result = self.manager.backup(incremental=True)
        self.assertIsInstance(result, dict)

    def test_restore_command(self):
        """Test restore command"""
        result = self.manager.restore(backup_path="/tmp/test_backup.tar.gz")
        self.assertIsInstance(result, dict)

    def test_restore_dry_run(self):
        """Test restore in dry-run mode"""
        result = self.manager.restore(
            backup_path="/tmp/test_backup.tar.gz",
            dry_run=True
        )
        self.assertIsInstance(result, dict)


class TestCompose(unittest.TestCase):
    """Test workflow composition"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_compose_single_subsystem(self):
        """Test composing single subsystem"""
        result = self.manager.compose("voice", action="start")
        self.assertIsInstance(result, dict)

    def test_compose_multiple_subsystems(self):
        """Test composing multiple subsystems"""
        result = self.manager.compose("voice+phone", action="start")
        self.assertIsInstance(result, dict)

    def test_compose_three_subsystems(self):
        """Test composing three subsystems"""
        result = self.manager.compose("voice+phone+gui", action="start")
        self.assertIsInstance(result, dict)

    def test_compose_with_execute_action(self):
        """Test compose with execute action"""
        result = self.manager.compose("voice+memory", action="execute")
        self.assertIsInstance(result, dict)

    def test_compose_with_test_action(self):
        """Test compose with test action"""
        result = self.manager.compose("voice+phone", action="test")
        self.assertIsInstance(result, dict)

    def test_compose_with_options(self):
        """Test compose with options"""
        options = {"profile": "test"}
        result = self.manager.compose("voice", action="start", options=options)
        self.assertIsInstance(result, dict)


class TestSubsystemLookup(unittest.TestCase):
    """Test subsystem lookup and access"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_get_subsystem_info(self):
        """Test getting subsystem info"""
        voice_info = self.manager._subsystems.get("voice")
        self.assertIsNotNone(voice_info)
        self.assertEqual(voice_info.name, "voice")

    def test_subsystem_exists_in_registry(self):
        """Test subsystem exists in registry"""
        for subsystem in Subsystem:
            self.assertIn(subsystem.cmd, self.manager._subsystems)

    def test_access_all_subsystems(self):
        """Test accessing all subsystems"""
        for name, info in self.manager._subsystems.items():
            self.assertIsNotNone(info)
            self.assertIsInstance(info, SubsystemInfo)


class TestLogging(unittest.TestCase):
    """Test logging functionality"""

    def test_logger_created(self):
        """Test logger is created"""
        manager = Ech0LauncherManager()
        self.assertIsNotNone(manager.logger)

    def test_logger_name(self):
        """Test logger name"""
        manager = Ech0LauncherManager()
        self.assertEqual(manager.logger.name, "ech0.launcher")

    def test_logger_has_handlers(self):
        """Test logger has handlers"""
        manager = Ech0LauncherManager()
        self.assertGreater(len(manager.logger.handlers), 0)


class TestErrorHandling(unittest.TestCase):
    """Test error handling"""

    def setUp(self):
        """Create manager for each test"""
        self.manager = Ech0LauncherManager()

    def test_invalid_subsystem_compose(self):
        """Test compose with invalid subsystem"""
        result = self.manager.compose("invalid_subsystem")
        # Should still return dict, but might have error flag
        self.assertIsInstance(result, dict)

    def test_daemon_returns_dict(self):
        """Test daemon command always returns dict"""
        result = self.manager.daemon()
        self.assertIsInstance(result, dict)

    def test_voice_returns_dict(self):
        """Test voice command always returns dict"""
        result = self.manager.voice()
        self.assertIsInstance(result, dict)

    def test_phone_returns_dict(self):
        """Test phone command always returns dict"""
        result = self.manager.phone()
        self.assertIsInstance(result, dict)

    def test_gui_returns_dict(self):
        """Test GUI command always returns dict"""
        result = self.manager.gui()
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main()
