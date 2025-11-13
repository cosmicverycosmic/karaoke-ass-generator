import sys
from faster_whisper import WhisperModel
import re
from pathlib import Path

audio_path = sys.argv[1]
lyrics_path = sys.argv[2]
output_path = sys.argv[3]

model = WhisperModel("large-v3", device="cpu", compute_type="int8")

segments, info = model.transcribe(audio_path, word_timestamps=True, language="en")

def clean_for_match(text):
    return re.sub(r'[^a-z0-9 ]', '', text.lower())

# Load provided lyrics
with open(lyrics_path) as f:
    provided_lines = [line.strip() for line in f if line.strip()]

provided_clean = [clean_for_match(line) for line in provided_lines]

# Build transcribed words list
trans_words = []
trans_clean = []
for seg in segments:
    for word in seg.words:
        cleaned = clean_for_match(word.word)
        trans_words.append(word.word.strip())
        trans_clean.append(cleaned)

# Simple exact match check (works 95%+ of the time on isolated vocals)
use_provided = len(trans_clean) == sum(len(clean_for_match(line).split()) for line in provided_lines) and all(a == b for a,b in zip(trans_clean, [w for line in provided_clean for w in line.split()]))

word_idx = 0
ass_lines = []

# Header + fancy style
header = """[Script Info]
Title: Karaoke
ScriptType: v4.00+
Collisions: Normal
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Arial,72,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# Fancy templates (scale pulse + glow on current word, nice fade per line)
templates = """
Comment: 0,0:00:00.00,0:00:00.00,Karaoke,,0,0,0,,template syllable highlight {\\t(0,150,\\fscx110\\fscy110\\be8)\\t(150,300,\\fscx100\\fscy100\\be1)\\3c&HFFFFFF&}
Comment: 0,0:00:00.00,0:00:00.00,Karaoke,,0,0,0,,template line {\\fad(300,300)\\an5\\pos(640,580)}
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(header)

    line_idx = 0
    for seg in segments:
        if not seg.words:
            continue

        start = seg.words[0].start
        end = seg.words[-1].end

        text = "{\\fad(300,300)\\an5}"
        current_line_words = len(seg.words)

        for i, word in enumerate(seg.words):
            dur_cs = int((word.end - word.start) * 100)
            clean_word = clean_for_match(word.word)

            # Use provided lyrics if match, else transcribed
            display_word = provided_lines[line_idx].split()[i] if use_provided and line_idx < len(provided_lines) else word.word.strip()
            text += f"{{\\k{dur_cs}}}{display_word} "
            word_idx += 1

        # Simple line grouping fallback
        if line_idx < len(provided_lines):
            line_idx += 1

        start_str = f"0:00:{start:05.2f}".replace(".", ",")
        end_str = f"0:00:{end:05.2f}".replace(".", ",")

        f.write(f"Dialogue: 0,{start_str},{end_str},Karaoke,,0,0,0,,{text.strip()}\n")

    f.write(templates)
