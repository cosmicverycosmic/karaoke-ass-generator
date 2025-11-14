from pyonfx import Ass

# Load the pre-templated ASS from Whisper
io = Ass("pre.ass")
meta, styles, lines = io.get_data()

# Very simple effect example:
# add a soft fade-in/fade-out to each Karaoke line.
for line in lines:
    if line.type == "Dialogue" and line.style == "Karaoke":
        # Prepend a fade override; keep existing \k timing intact.
        line.text = r"{\fad(200,200)}" + line.text

# Write to final.ass
io.write("final.ass")
