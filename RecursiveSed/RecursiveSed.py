#!/usr/bin/python3.11

import os
import re
from time import sleep
from pathlib import Path
from argparse import ArgumentParser

def replace(line, original, substitute):
    insensitive =  re.compile(re.escape(original), re.IGNORECASE)
    return insensitive.sub(substitute, line)

def case_insensitive_match(term, in_something):
        matcher = re.compile(term, re.IGNORECASE)
        if any(filter(matcher.match, in_something)):
            return True
        return False


class RecursiveChanger:
    def __init__(self, original, substitute, change_filename):
        self.original = original
        self.substitute = substitute
        self.change_filename = change_filename
        self.directories = []

    def recurse(self, path):
        for _ in Path(path).rglob('*'):
            if os.path.isfile(_):
                print(f"Replacing file: {_}")
                self.change_file(_)
        for folder, replaced in set(self.directories):
            os.system(f'mv {str(folder)} {str(replaced)}')

    def folder_change(self, folder):
        parent, folder = folder.parent, folder.name
        if self.original in folder: #no case insensitive for folder
            replaced = os.path.join(parent, replace(folder, self.original, self.substitute))
            self.directories.append((folder, replaced))
        else:
            self.folder_change(parent)

    def change_file(self, file):
        try:
            lines = [line for line in open(file)]
        except UnicodeDecodeError:
            return
        except Exception as E:
            print(E)
        if not self.change_filename and case_insensitive_match(self.original, str(file)):
            if self.original in str(file.parent) and not case_insensitive_match(self.original, str(file.name)): #string in folder and no case insensitive for folder
                folder, filename = file.parent, file.name
                self.folder_change(folder)
                return "BECAUSE ITS A FOLDER"
            else: #string in file
                folder, filename = file.parent, file.name
                filename = replace(str(filename), self.original, self.substitute)
                new_file = os.path.join(folder, filename)
                os.system(f'mv {str(file)} {str(new_file)}')
                file = new_file
        with open(str(file), 'w+') as f:
            for line in lines:
                f.write(replace(line, self.original, self.substitute))

parser = ArgumentParser()
parser.add_argument('-o', '--original', required=True, help="String to be replaced")
parser.add_argument('-s', '--substitute', required=True, help="String to be replaced with")
parser.add_argument('-f', '--filename', action='store_true', help="Dont replace filename")
parser.add_argument('--path', help="Directory path to be changed. If not provided then CWD is taken")
args = parser.parse_args()

changer = RecursiveChanger(args.original, args.substitute, args.filename)
if args.path:
    path = args.path
else:
    path = os.getcwd()
changer.recurse(path)
