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

def find_value(kb, find):
    if kb.part_of_facts(find):
        return True
    results = list()
    for rule in kb.associated_rules(find):
        for i in range(len(rule)):
            if not is_connective(rule[i]) and rule[i] != find:
                results.append(find_value(kb, rule[i]))
                if not isinstance(results[i], bool) and results[i] != None:
                    print("expert-system: Error: Value found is not Bool or None.")
                print(rule[i] + " " + str(results[i]))
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
        elif len(results) < 3:
            print("expert-system: Error: Rule end result should consist of at least 3 parts.")
        elif "|" in results:
            return None
        elif "!" in results:
            return None if result[0] is None else not results[0]
        else:
            return results[0]
    return False

def search_answer(kb):
    for query in kb.iterate_queries():
        answer = find_value(kb, query)
        print(query + " = " + str(answer))
