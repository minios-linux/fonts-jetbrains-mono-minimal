#!/usr/bin/env python3
"""Check the four real desktop styles and core multilingual coverage."""

from pathlib import Path
import sys
from fontTools.ttLib import TTFont


directory, prefix, suffix = sys.argv[1:]
for style, bold, italic in (
    ("Regular", False, False), ("Bold", True, False),
    ("Italic", False, True), ("BoldItalic", True, True),
):
    path = Path(directory) / (prefix + "-" + style + "." + suffix)
    font = TTFont(str(path))
    try:
        assert bool(font["head"].macStyle & 1) == bold, path
        assert bool(font["head"].macStyle & 2) == italic, path
        assert (font["OS/2"].usWeightClass >= 700) == bold, path
        cmap = font.getBestCmap()
        assert all(ord(char) in cmap for char in "ABCxyz012АБВабвΑΒΓαβγ€"), path
        assert "fvar" not in font, path
        if prefix == "JetBrainsMono":
            assert font["post"].isFixedPitch, path
            metrics = font["hmtx"].metrics
            assert len({metrics[cmap[ord(char)]][0] for char in "Wi0 Аα"}) == 1, path
    finally:
        font.close()
    print("PASS:", path)
print("4 font style/coverage checks passed")
