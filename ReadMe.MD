# Karaoke ASS Generator 🎤 (2025 edition)

One-click pro-level English karaoke subtitles with per-word highlight effects — completely free on GitHub Actions.

### Features
- Vocal isolation → super accurate word timings on real songs
- Modern fancy effects via Aegisub Karaoke Templater (scale pulse + glow + color sweep)
- Word-level (perfect for karaoke)
- English only, singing-aware
- Two ways to run:
  1. Quick — no files in repo (paste lyrics + audio URL)
  2. Classic — commit your song.mp3 + lyrics.txt

### Quick start (no commit needed)
1. Click **"Use this template"** → create your own repo
2. Go to **Actions** → "Generate Karaoke ASS" → **Run workflow**
3. Choose **"Provide audio URL and paste lyrics (no commit needed)"**
4. Paste your lyrics (one line per subtitle line)
5. Paste a direct download link to your song (mp3/wav)  
   Examples that work:
   - Dropbox: add `?dl=1` to the share link
   - Google Drive: change `/open?id=FILEID` → `/uc?export=download&id=FILEID`
   - Any direct .mp3/.wav link
6. Click **Run workflow**
7. Wait ~10-25 min → download `final.ass` from Artifacts

### Classic way (commit files)
Just drop `song.mp3` (or .wav) and `lyrics.txt` into the repo root, then run the workflow with default settings.

### Example lyrics.txt
Twinkle twinkle little star
How I wonder what you are
Up above the world so high
Like a diamond in the sky
text### Result
- Bottom-centered, clean Arial 72
- Line fade in/out
- Current word pulses + glows + color sweep (blue → white)
- Ready for any player/editor

### Customization
Want different colors/position/effects? Edit the `templates` block at the bottom of `generate_ass.py`.

Enjoy! Drop a star if you make something cool ✨
