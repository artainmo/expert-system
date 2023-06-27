import sys
import os
from src.parsing import KnowledgeBase
from src.inference_engine import search_answer

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("expert-system: Error: Wrong number of program arguments. Program takes one file as input.")
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print("expert-system: Error: '%s' is not an existing file." % sys.argv[1])
        sys.exit(1)
    with open(sys.argv[1], "r") as fd:
        knowledge_base = KnowledgeBase()
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
    search_answer(knowledge_base)
