def connective_result(leftPart, connective, rightPart):
        if (not isinstance(leftPart, bool) and leftPart != None) \
                    or (not isinstance(rightPart, bool) and rightPart != None):
            print("expert-system: Error: Connective is not preceded and followed by Bools or Nones.")
        if connective == "+":
            if leftPart is None or rightPart is None:
                return None
            else:
                return leftPart and rightPart
        elif connective == "|":
            if (leftPart is None and rightPart is not True) or \
                        (rightPart is None and leftPart is not True):
                return None
            else:
                 return leftPart or rightPart
        elif connective == "^":
            if leftPart is None or rightPart is None:
                return None
            else:
                return leftPart ^ rightPart
        else:
            print("expert-system: Error: Internal Error: 'connective_result' function unknown connective.")

def is_connective(word):
    if (word == "+" or word == "|" or word == "^" or word == "!"
                or word == "=>" or word == "<==>"):
        return True
    else:
        return False

def find_value(kb, find, reasoning, depth):
    reasoning.append((depth, "Find value of %s." % find))
    if kb.part_of_facts(find):
        reasoning.append((depth, "%s is part of initial facts." % find))
        return True
    else:
        reasoning.append((depth, "%s is not part of initial facts." % find))
    results = list()
    for rule in kb.associated_rules(find):
        reasoning.append((depth, "%s has associated rule: %s." % (find, kb.rule_to_string(rule))))
        for i in range(len(rule)):
            if not is_connective(rule[i]) and rule[i] != find:
                results.append(find_value(kb, rule[i], reasoning, depth + 1))
                if not isinstance(results[i], bool) and results[i] != None:
                    print("expert-system: Error: Value found is not Bool or None.")
                reasoning.append((depth, "Now we know %s is %s. ( %s)" \
                            % (rule[i], results[i], \
                            kb.rule_to_string_with_answers(rule, results))))
            else:
                results.append(rule[i])
        i = 0
        while i < len(results):
            if is_connective(results[i]):
                if results[i] == "=>" or results[i] == "<==>":
                    break
                elif results[i] == "!":
                    if i + 1 >= len(results) or \
                                (not isinstance(results[i+1], bool) and results[i+1] != None):
                        print("expert-system: Error: Rule uses ! without following Bool or None.")
                    results[i+1] = None if results[i+1] is None else not results[i+1]
                    del results[i]
                else:
                    if i + 1 >= len(results) or i - 1 < 0:
                        print("expert-system: Error: Rule uses connective without following or preceding value.")
                    results[i+1] = connective_result(results[i-1], results[i], results[i+1])
                    del results[i-1:i+1]
                    i -= 1
            i += 1
        if not isinstance(results[0], bool) and results[0] != None:
            print("expert-system: Error: End result of a value is not Bool or None.")
            exit(1)
        elif len(results) < 3:
            print("expert-system: Error: Rule end result should consist of at least 3 parts.")
            exit(1)
        elif "|" in results:
            return None
        elif "!" in results:
            return None if result[0] is None else not results[0]
        else:
            return results[0]
    reasoning.append((depth, "%s is not part of initial facts nor can its value be deduced from rules." % find))
    return False

def search_answer(kb, show_reasoning):
    reasoning = list()
    for query in kb.iterate_queries():
        answer = find_value(kb, query, reasoning, 0)
        reasoning.append((0, "For query %s the final answer is: %s\n" % (query, answer)))
        if show_reasoning:
            for part in reasoning:
                for _ in range(part[0]):
                    print(" ", end="")
                print(part[1])
        else:
            print(reasoning[-1][1])
