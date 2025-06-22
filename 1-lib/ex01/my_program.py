from path import Path

folder = Path("my_folder")
folder.makedirs_p()

file = folder / "my_file.txt"

file.write_text("Hello World from Agvan")

content = file.read_text()
print(content)