import pytest
from media import surround_downmix as mod

CASES = [
    ("phase", 'm.phase_align(1.0, 0.5) == approx(0.5)'),
    ("lfe", 'm.lfe_attenuation(2.0, 0.5) == approx(1.0)'),
    ("count", 'm.channel_count("5.1") == 6'),
    ("count71", 'm.channel_count("7.1") == 8'),
    ("center", 'm.center_priority(1.0, 2.0, 3.0) == approx(7.0)'),
    ("peak", 'm.true_peak_limit(2.0, 1.0) == approx(1.0)'),
    ("mono", 'm.mono_coeff(True) == approx(0.5)'),
    ("mono_false", 'm.mono_coeff(False) == approx(1.0)'),
    ("matrix", 'm.matrix_for_layout("5.1") == "5.1"'),
    ("dialogue_default", 'm.dialogue_metadata(None, 0.0) == approx(0.0)'),
    ("dialogue_value", 'm.dialogue_metadata(1.0, 0.0) == approx(1.0)'),
    ("delay", 'm.delay_for_rate(48000, 24000) == 2'),
    ("domain", 'm.time_domain("time") is True'),
    ("multitrack", 'm.multitrack([1, 2, 3]) == 3'),
    ("cache", 'm.cache_matrix("5.1", "v1") == "5.1#v1"')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
