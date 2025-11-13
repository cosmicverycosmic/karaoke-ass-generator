Karaoke ASS Generator 🎤

Turn any English song + plain lyrics into a pro-level karaoke .ass file with beautiful per-word effects — completely automatically and for free using GitHub Actions.


What it does
1. Isolates vocals with **Demucs** (so Whisper isn't confused by instruments)
2. Runs **faster-whisper large-v3** (int8 CPU) on the clean vocals → extremely accurate word-level timestamps for singing
3. Generates a clean pre-template .ass with one highlighted word per `\k` duration
4. Applies **Aegisub's Karaoke Templater** (headless via aegisub-cli) with a modern built-in template:
   - Gradient color sweep (blue → white)
   - Current word pulse + glow/blur
   - Line fade-in/out
   - Bottom-centered, clean Arial style

Result: a ready-to-use `final.ass` you can drop on any video.

Features
- English only (best accuracy)
- Word-level timing (perfectly usable for karaoke, no syllable splitting needed)
- Singing-aware (vocal isolation = much better than plain Whisper on full mix)
- Zero local setup — everything runs on GitHub's servers
- No API keys, no cost
- Built-in fancy template (easily customizable)

How to use

Option 1 – Use this repo as a template (recommended)
1. Click **"Use this template"** → Create a new repository
2. Clone it locally or just work in GitHub web editor

Option 2 – Fork or copy the files manually
Just make sure you have this exact structure:

karaoke-ass-generator/
├── .github/workflows/generate-karaoke.yml
├── generate_ass.py
├── lyrics.txt          # ← your lyrics here
├── song.mp3            # ← your audio here (mp3 or wav)
└── README.md


Add your files
- `song.mp3` or `song.wav` in the repo root
- `lyrics.txt` — plain text, **one lyric line per line**, exact capitalization/punctuation doesn't matter but wording must match the sung words.

Example `lyrics.txt`:
Twinkle twinkle little star
How I wonder what you are
Up above the world so high
Like a diamond in the sky

Run the workflow
1. Go to the **Actions** tab
2. Select **"Generate Karaoke ASS"**
3. Click **Run workflow**
   - You can change the file names in the inputs if you named them differently (default: `song.mp3` and `lyrics.txt`)
4. Wait 8–25 minutes (depends on song length; CPU-only transcription)
5. When it finishes, download the artifact **karaoke-ass** → inside is `final.ass`

Use the .ass file

ffmpeg -i video.mp4 -vf "ass=final.ass" -c:v libx264 -crf 23 output.mkv

or just drag it onto MPC-HC, VLC (with subtitles enabled), or any editor (DaVinci, Premiere, etc.).

Example output (template look)

The default template produces something like this classic modern style:

- Line fades in/out with `{\fad(300,300)}`
- Bottom center (`\an5\pos(640,580)`)
- Highlighted word sweeps from blue to white, pulses 110 % + temporary glow
- Filled word is bright white, past words dim cyan

If you want a different look (romaji style, top-aligned, particles, etc.), just edit the `templates` block at the bottom of `generate_ass.py`.

Customization

- Change colors, fonts, position: edit the `Style:` line and the template comments in `generate_ass.py`
- Use a completely different template set: replace the entire `templates = """..."""` block with your favorite one (copy from any Aegisub karaoke file)
- Want syllables instead of words? Change `--syllables` flag or use a different aligner (PR welcome!)

Limitations & Tips
- English only right now (Whisper language fixed to "en")
- Works best on pop, rock, clear vocals (vocal isolation helps a lot)
- If lyrics have a lot of "ooh/aah" or very fast rap, you may need to manually fix a few timings (open the generated `pre.ass` before templater if you want to tweak)
- GitHub Actions free tier gives you ~2000 minutes/month — plenty for personal use
- First run on a new repo may take longer because of model download (~4 GB for Whisper large-v3)

Tech stack (all open-source)
- Demucs (htdemucs) – vocal separation
- faster-whisper large-v3 int8 – transcription + word timestamps
- aegisub-cli – headless Karaoke Templater
- Python 3.11 + torch CPU in GitHub Actions

Credits & Thanks
- Myaamori for aegisub-cli
- Guillefix & faster-whisper team
- Demucs team @ Meta
- Original Karaoke Templater authors

Enjoy your karaoke parties! 🚀

If you make something cool with this, drop a star or share a video — I'd love to see it.


Just copy this entire text into `README.md` in your repo. It’s ready to go, looks great on GitHub, and explains everything a user needs.
