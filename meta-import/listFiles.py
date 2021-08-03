import os

with open("files.txt", "w", encoding="utf-8", newline="\n") as outputFile:
    for root, folders, files in os.walk(os.path.join("~/kwz/")):
        for file in files:
            if str(file).endswith(".kwz"):
                outputFile.write(os.path.join(root, file) + "\n")
