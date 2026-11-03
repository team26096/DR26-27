"""Offline checks for mission attachment ownership; never contacts a robot."""
import contextlib
import importlib
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


ROOT = Path(__file__).resolve().parents[1]


class AttachmentLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.open_ports = {}
        self.created = []
        self.fail_port = None

        def motor(port, *args, **kwargs):
            if port == self.fail_port:
                raise RuntimeError('attachment missing')
            if port in self.open_ports:
                raise OSError(16, 'Device or resource busy')
            device = MagicMock()
            device.angle.return_value = 42
            device.done.return_value = True
            device.close.side_effect = lambda: self.open_ports.pop(port)
            self.open_ports[port] = device
            self.created.append((port, kwargs.get('gears')))
            return device

        self.base = MagicMock()
        self.base.settings.return_value = (400, 200, 200, 200)
        self.base.heading_control.pid.return_value = (100, 0, 10, 0, 0)
        self.base.done.return_value = True
        self.base.angle.return_value = 0
        self.base.distance.return_value = 0
        hub = MagicMock()
        hub.system.info.return_value = {'name': 'PixieBricks'}
        hub.system.name.return_value = 'PixieBricks'
        hub.battery.voltage.return_value = 8000
        hub.imu.heading.return_value = 0
        watch = MagicMock()
        watch.time.return_value = 100
        modules = {}
        for name in ('pybricks', 'pybricks.hubs', 'pybricks.pupdevices',
                     'pybricks.parameters', 'pybricks.robotics', 'pybricks.tools'):
            modules[name] = types.ModuleType(name)
        modules['pybricks'].version = 'offline'
        modules['pybricks.hubs'].PrimeHub = lambda: hub
        modules['pybricks.pupdevices'].Motor = motor
        modules['pybricks.parameters'].Port = types.SimpleNamespace(A='A', B='B', C='C', E='E')
        modules['pybricks.parameters'].Direction = MagicMock()
        modules['pybricks.parameters'].Stop = MagicMock()
        modules['pybricks.robotics'].DriveBase = lambda *a, **kw: self.base
        modules['pybricks.tools'].StopWatch = lambda: watch
        modules['pybricks.tools'].wait = lambda ms: None
        self.menu = MagicMock()
        modules['pybricks.tools'].hub_menu = self.menu
        # Keep imports isolated from other tests and any installed Pybricks package.
        self.module_patch = patch.dict(sys.modules, modules)
        self.module_patch.start()
        self.addCleanup(self.module_patch.stop)
        for name in ('helpers', 'config', 'main', *(p.stem for p in ROOT.glob('run*.py'))):
            sys.modules.pop(name, None)
        self.path_patch = patch.object(sys, 'path', [str(ROOT), *sys.path])
        self.path_patch.start()
        self.addCleanup(self.path_patch.stop)
        self.config = importlib.import_module('config')
        self.helpers = importlib.import_module('helpers')

    def test_all_runs_repeat_through_real_menu_without_busy_ports(self):
        class MenuFinished(Exception):
            pass

        self.menu.side_effect = [*self.config.RUNS, *self.config.RUNS, MenuFinished()]
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(MenuFinished):
            importlib.import_module('main')
        self.assertEqual(set(self.open_ports), {'A', 'E'})
        expected = [
            ('B', [[12, 20], [12, 12]]), ('C', [[12, 20], [12, 12]]),
            ('C', [[12, 20], [12, 20]]), ('B', [[12, 20], [12, 36]]),
            ('C', [[12, 20], [12, 20]]), ('B', [[12, 20], [12, 36]]),
            ('B', [[12, 20], [20, 20]]), ('C', [[12, 20], [1, 24]]),
            ('C', [[12, 20]]), ('B', [[12, 20], [12, 36]]),
            ('C', [[12, 36]]),
        ]
        self.assertEqual(self.created[2:], expected * 2)

    def test_standalone_run_releases_attachments_on_motion_error(self):
        for number in ('3', '4', '5', '6', '8', '9'):
            with self.subTest(run=number):
                self.base.straight.side_effect = RuntimeError('motion failed')
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(RuntimeError, 'motion failed'):
                    self.helpers.run_alone(self.config.RUNS[number])
                self.assertEqual(set(self.open_ports), {'A', 'E'})
                self.base.stop.assert_called()

    def test_first_attachment_is_closed_if_second_cannot_open(self):
        self.fail_port = 'B'  # Research Platform opens C first, then B.
        with self.assertRaisesRegex(RuntimeError, 'attachment missing'):
            self.helpers.run_alone(self.config.RUNS['4'])
        self.assertEqual(set(self.open_ports), {'A', 'E'})


if __name__ == '__main__':
    unittest.main()
