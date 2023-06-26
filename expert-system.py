import sys
import os
from src.parsing import Parsing

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("expert-system: Error: Wrong number of program arguments. Program takes one file as input.")
        sys.exit(1)
    if os.path.isfile(sys.argv[1]) is False:
        print("expert-system: Error: '%s' is not an existing file." % sys.argv[1])
        sys.exit(1)
    with open(sys.argv[1], "r") as fd:
        parsing = Parsing()
        for line in fd.readlines():
            print(line, end="")
            if line[0] == '\n' or line[0] == '#':
                pass
            elif line[0] == '=':
                parsing.add_facts(line)
            elif line[0] == '?':
                parsing.add_queries(line)
            else:
                parsing.add_rule(line)
    print("\n")
    print(parsing)
