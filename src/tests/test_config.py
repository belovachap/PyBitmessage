"""
Various tests for config
"""
from __future__ import absolute_import

import os
import unittest

from pybitmessage.bmconfigparser import BMConfigParser
from .test_process import TestProcessProto


class TestConfig(unittest.TestCase):
    """A test case for bmconfigparser"""

    def test_safeGet(self):
        """safeGet retuns provided default for nonexistent option or None"""
        self.assertIs(
            BMConfigParser().safeGet('nonexistent', 'nonexistent'), None)
        self.assertEqual(
            BMConfigParser().safeGet('nonexistent', 'nonexistent', 42), 42)

    def test_safeGetBoolean(self):
        """safeGetBoolean returns False for nonexistent option, no default"""
        self.assertIs(
            BMConfigParser().safeGetBoolean('nonexistent', 'nonexistent'),
            False
        )
        # no arg for default
        with self.assertRaises(TypeError):
            BMConfigParser().safeGetBoolean(
                'nonexistent', 'nonexistent', True)

    def test_safeGetInt(self):
        """safeGetInt retuns provided default for nonexistent option or 0"""
        self.assertEqual(
            BMConfigParser().safeGetInt('nonexistent', 'nonexistent'), 0)
        self.assertEqual(
            BMConfigParser().safeGetInt('nonexistent', 'nonexistent', 42), 42)


class TestProcessConfig(TestProcessProto):
    """A test case for keys.dat"""

    def test_config_defaults(self):
        """Test settings in the generated config"""
        self._stop_process()
        config = BMConfigParser()
        config.read(os.path.join(self.home, 'keys.dat'))

        self.assertEquals(config.safeGetInt(
            'bitmessagesettings', 'settingsversion'), 10)
        self.assertEquals(config.safeGetInt(
            'bitmessagesettings', 'port'), 8444)
        # don't connect
        self.assertTrue(config.safeGetBoolean(
            'bitmessagesettings', 'dontconnect'))
        # API disabled
        self.assertFalse(config.safeGetBoolean(
            'bitmessagesettings', 'apienabled'))

        # extralowdifficulty is false
        self.assertEquals(config.safeGetInt(
            'bitmessagesettings', 'defaultnoncetrialsperbyte'), 1000)
        self.assertEquals(config.safeGetInt(
            'bitmessagesettings', 'defaultpayloadlengthextrabytes'), 1000)
