"""
test_rules.py
agent/rules.json butunlugu: yapi + ihlal edilemez emniyet/timing kurallari yerinde mi.
Bu kurallar agent'in karakterinin cekirdegi; sessizce kaybolmalari regresyon olur.
"""
import json
import unittest

from _common import RULES

REQUIRED_SECTIONS = ['knowledge', 'timing', 'safety', 'code_quality',
                     'naming', 'documentation', 'protocol_selection',
                     'hmi_design', 'project_output']


class TestRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rules = json.loads(RULES.read_text())

    def test_valid_json_with_all_sections(self):
        for sec in REQUIRED_SECTIONS:
            self.assertIn(sec, self.rules, f"rules.json '{sec}' bolumu eksik")

    def test_safety_invariants_are_true(self):
        nv = self.rules['safety']['never_violate']
        # Bu bes kural emniyet felsefesinin temeli — hicbiri False/eksik olamaz
        for k in ('safety_io_on_standard_modules_forbidden',
                  'all_outputs_deenergize_on_cpu_fault',
                  'estop_is_hardwired_not_software',
                  'fail_safe_default_is_stop_not_run',
                  'watchdog_always_enabled'):
            self.assertTrue(nv.get(k) is True,
                            f"safety.never_violate.{k} True olmali")

    def test_timing_targets_are_ordered(self):
        t = self.rules['timing']['task_cycle_targets_ms']
        order = ['safety_signals', 'motion_drive_control', 'fast_interlock',
                 'analog_pid', 'hmi_comms', 'logging_telemetry']
        vals = [t[k]['max_ms'] for k in order]
        self.assertEqual(vals, sorted(vals),
                         "task_cycle_targets_ms max_ms degerleri artan sirada olmali")
        self.assertEqual(t['safety_signals']['max_ms'], 1,
                         "Emniyet sinyali hedefi 1 ms olmali")

    def test_timing_blocking_io_rule(self):
        r = self.rules['timing']['rules']
        self.assertTrue(r.get('blocking_io_in_freewheeling_only'))
        self.assertTrue(r.get('never_disable_watchdog_to_fix_overrun'))
        self.assertLessEqual(r.get('total_cpu_load_target_percent_max', 100), 80)

    def test_naming_convention(self):
        n = self.rules['naming']
        self.assertIn('format', n)
        self.assertEqual(n.get('max_length'), 24)
        self.assertTrue(n.get('no_spaces'))

    def test_decisions_use_triple_format(self):
        triple = self.rules['documentation']['decisions_use_triple_format']
        self.assertEqual(triple, ['KARAR', 'GEREKÇE', 'TAKAS'])

    def test_hmi_is_protocol_bridged_not_embedded(self):
        h = self.rules['hmi_design']
        self.assertTrue(h.get('bridge_is_always_protocol'))
        self.assertTrue(h.get('logic_never_embedded_in_hmi'))


if __name__ == '__main__':
    unittest.main()
