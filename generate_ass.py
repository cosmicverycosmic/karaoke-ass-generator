import sys
import re
import datetime
from faster_whisper import WhisperModel

def ass_time(seconds: float) -> str:
    td = datetime.timedelta(seconds=seconds)
    hours, rem = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(rem, 60)
    millis = int(td.microseconds / 10000)
    return f"0:{int(minutes):02}:{int(seconds):02}.{millis:02}"

model = WhisperModel("large-v3", device="cpu", compute_type="int8")
segments, _ = model.transcribe("vocals.wav", word_timestamps=True, language="en")

# Collect all timed words from Whisper
words = [w for seg in segments for w in seg.words if w.word.strip()]

def clean(text: str) -> str:
    return re.sub(r'[^a-z0-9]', '', text.lower())

trans_clean = [clean(w.word) for w in words]

# Load provided lyrics
with open("lyrics.txt", encoding="utf-8") as f:
    provided_lines = [line.strip() for line in f if line.strip()]

provided_display_groups = []   # list of lists: original words with punctuation/casing
provided_clean_flat = []
for line in provided_lines:
    display_words = line.split()
    provided_display_groups.append(display_words)
    provided_clean_flat.extend(clean(w) for w in display_words)

# Decide if we can trust the provided lyrics
total_trans = len([c for c in trans_clean if c])
total_prov = len([c for c in provided_clean_flat if c])
use_provided = (10 < total_trans == total_prov and 
                all(a == b for a, b in zip(trans_clean, provided_clean_flat) if a and b))

header = """[Script Info]
Title: Karaoke
ScriptType: v4.00+
Collisions: Normal
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Arial,72,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,0,2,10,10,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# Modern fancy template (color sweep + scale pulse + glow on current word)
templates = """
Comment: 0,0:00:00.00,0:00:00.00,Karaoke,,0,0,0,,{\\fad(350,350)\\an5\\pos(640,660)}
Comment: 0,0:00:00.00,0:00:00.00,Karaoke,,0,0,0,,template all {\\1c&HAAAAAA&\\3c&H888888&}
Comment: 0,0:00:00.00,0:00:00.00,Karaoke,,0,0,0,,template syl {\\t(0,120,\\fscx112\\fscy112\\be10\\1c&H00FFFF&\\3c&HFFFFFF&)\\t(120,240,\\fscx100\\fscy100\\be1)}
"""

with open("pre.ass", "w", encoding="utf-8") as f:
    f.write(header)

    if use_provided and provided_display_groups:
        ptr = 0
        for display_words in provided_display_groups:
            if ptr + len(display_words) > len(words):
                break
            group = words[ptr:ptr + len(display_words)]
            if not group:
                continue
            start = group[0].start
            end = group[-1].end
            line_text = ""
            prev = start
            for i, w in enumerate(group):
                # small gap filler (rare)
                if w.start > prev + 0.02:
                    line_text += "{\\kf%d}" % int((w.start - prev) * 100)
                dur_cs = max(1, int((w.end - w.start) * 100))
                line_text += "{\\k%d}%s " % (dur_cs, display_words[i])
                prev = w.end
            f.write(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Karaoke,,0,0,0,,{line_text}\n")
            ptr += len(display_words)
    else:
        # Fallback: Whisper's own segmentation
        for seg in segments:
            if not seg.words:
                continue
            start = seg.words[0].start
            end = seg.words[-1].end
            line_text = ""
            for w in seg.words:
                dur_cs = max(1, int((w.end - w.start) * 100))
                line_text += "{\\k%d}%s " % (dur_cs, w.word.strip())
            f.write(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Karaoke,,0,0,0,,{line_text}\n")

    f.write(templates)
