import os
import re

class Marker :
    def __init__(self) :
        self.pattern = re.compile(".md$|.markdown$")
    def mark(self) :
        md_files = []
        for root, dir, files in os.walk(".") :
            for file in files :
                if self.pattern.search(file) is not None :
                    md_files.append(root + file)
        return md_files
