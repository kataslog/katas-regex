#!/usr/bin/python

import sys, urllib, json, re

BASE_URL = "https://raw.githubusercontent.com/kataslog/katas-regex/master/mentor"

OKCODE = "\033[92m"
FAILCODE = "\033[91m"
ENDC = "\033[0m"

def INCORRECT_ARGUMENTS():
    print "incorrect running arguments"

def fetch_test_data(name):
    url = "%s/tests/%s.json" % (BASE_URL, name)
    return fetch_json_data(url)

def fetch_hint_data(name):
    url = "%s/hints/%s.json" % (BASE_URL, name)
    return fetch_json_data(url)

def fetch_json_data(url):
    return json.loads(urllib.urlopen(url).read())

def fetch_solution(path, name):
    full_path = "%s/%s.txt" % (path, name)
    with open(full_path) as f:
        lines = filter(lambda line: not line.startswith('#') and line != '', map(lambda l: l.strip(), f.read().splitlines()))
        if len(lines) > 1:
            print "Incorrect solution. More than one solution strings."
            sys.exit(1)

        return lines[0]

def test(path, name):
    test_data = fetch_test_data(name)
    solution = fetch_solution(path, name)

    regex = re.compile(solution)
    correct_count = 0
    for test in test_data:
        line = test["line"]
        is_correct = regex.match(line) == test("correct")

        print_result(line, is_correct)
        correct_count += 1 if is_correct else 0

    incorrect_count = len(test_data) - correct_count
    print_stats(correct_count, incorrect_count)


def test_all(path):
    print "test all!"
    return

def hint(name):
    hints = fetch_hint_data(name)
    for hint in hints:
        print hint

def print_result(text, is_correct):
    code, symbol = (OKCODE, u"\u2713") if is_correct else (FAILCODE, u"\u2717")
    print "%s%s  %s%s" % (code, symbol, text, ENDC)

def print_stats(correct, incorrect):
    incorrect_string = "0" if incorrect == 0 else "%s%d%s" % (FAILCODE, incorrect, ENDC)
    print "\nCorrect count: %d\nIncorrect count: %s" % (correct, incorrect_string)

def run(path, command, kata):
    if command == "test":
        if not kata is None:
            test(path, kata)
        else:
            test_all(path)
        return

    if command == "hint":
        hint(kata)
        return

def prepare_args(args):
    path = args[1] if len(args)>1 else None
    command = args[2] if len(args)>2 else None
    kata = args[3] if len(args)>3 else None

    if command not in ["test", "hint"] or (command == "hint" and not kata is None):
        INCORRECT_ARGUMENTS()
        sys.exit(1)

    return (path, command, kata)

path, command, kata = prepare_args(sys.argv)
run(path, command, kata)
