from pyonfx import Ass

io = Ass("pre.ass")
meta, styles, lines = io.get_data()

for line in lines:
    if line.type == "Dialogue" and line.style == "Karaoke":
        # Simple global fade; your \k word timing from generate_ass.py stays intact
        line.text = r"{\fad(200,200)}" + line.text

io.write("final.ass")
