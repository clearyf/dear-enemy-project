import pandas as pd

import t_tests

def test_a():
    table = t_tests.read_short_video_data(t_tests.short_videos)
    assert len(table.columns) == 20
