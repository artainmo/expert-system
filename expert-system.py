import sys
import os
from src.parsing import KnowledgeBase
from src.inference_engine import search_answer

if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("expert-system: Error: Wrong number of program arguments. Program takes one file as input that can be preceded by a flag.")
        sys.exit(1)
    if not os.path.isfile(sys.argv[1 if len(sys.argv) == 2 else 2]):
        print("expert-system: Error: '%s' is not an existing file." % sys.argv[1])
        sys.exit(1)
    show_reasoning = False
    debug = False
    if len(sys.argv) == 3:
        if sys.argv[1] == "-v":
            show_reasoning = True
        elif sys.argv[1] == "-d":
            debug = True
        else:
            print("Unknown flag: %s. Use -v or -d." % sys.argv[1])
            exit(1)
    with open(sys.argv[1 if len(sys.argv) == 2 else 2], "r") as fd:
        knowledge_base = KnowledgeBase()
        print("\033[96mInput File:\033[0m")
        for line in fd.readlines():
            print(line, end="")
            if line[0] == '\n' or line[0] == '#':
                pass
            elif line[0] == '=':
                knowledge_base.add_facts(line)
            elif line[0] == '?':
                knowledge_base.add_queries(line)
            else:
                knowledge_base.add_rule(line)
    print("\n")
    print(knowledge_base)
    print("\033[96mAnswers:\033[0m")
    search_answer(knowledge_base, show_reasoning, debug)
