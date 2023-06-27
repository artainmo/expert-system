def add_db(kb, final, find):
    if final == None:
        kb.add_deduced_undetermined_fact(find)
    elif final == False:
        kb.add_deduced_inverse_fact(find)
    elif final == True:
        kb.add_deduced_fact(find)
    else:
        print("expert-system: Error: Final is not Bool or None.")
        exit(1)
    return final

def already_visited(rule, visited):
    for part in rule:
        if part == "=>":
            break
        if part in visited:
            return True
    return False

def connective_result(leftPart, connective, rightPart):
        if (not isinstance(leftPart, bool) and leftPart != None) \
                    or (not isinstance(rightPart, bool) and rightPart != None):
            print("expert-system: Error: Connective is not preceded (%s) and followed (%s) by Bools or Nones." % (leftPart, rightPart))
            exit(1)
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
            exit(1)

def is_connective(word):
    if (word == "+" or word == "|" or word == "^" or word == "!" or word == "=>"):
        return True
    else:
        return False

def clean_exclamations(results):
    i = 0
    while i < len(results):
        if results[i] == "=>":
            break
        elif results[i] == "!":
            if i + 1 >= len(results) or \
                        (not isinstance(results[i+1], bool) and results[i+1] != None):
                print("expert-system: Error: Rule uses ! without following Bool or None.")
                exit(1)
            results[i+1] = None if results[i+1] is None else not results[i+1]
            del results[i]
        i += 1

def solve_connectives(results):
    i = 0
    while i < len(results):
        if is_connective(results[i]):
            if results[i] == "=>":
                break
            elif results[i] == "!":
                print("expert-system: Error: ! should have been cleaned while solving connectives.")
                exit(1)
            else:
                if i + 1 >= len(results) or i - 1 < 0:
                    print("expert-system: Error: Rule uses connective without following or preceding value.")
                    exit(1)
                results[i+1] = connective_result(results[i-1], results[i], results[i+1])
                del results[i-1:i+1]
                i -= 1
        i += 1

def deduce(rule):
    clean_exclamations(rule)
    #TODO: Handle parantheses
    solve_connectives(rule)

def find_value(kb, find, reasoning, depth, visited, debug): #Uses depth first search (https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/)
    if debug:
        if input("You are searching %s at a depth of %d. Do you want to continue (y/n)? " % (find, depth)) == "n":
            print_reasoning(reasoning)
            exit(1)
    visited.append(find)
    reasoning.append((depth, "Find value of %s." % find))
    if kb.part_of_facts(find):
        reasoning.append((depth, "%s is part of initial facts." % find))
        return True
    elif kb.part_of_deduced_facts(find):
        reasoning.append((depth, "%s is part of deducted facts." % find))
        return True
    elif kb.part_of_deduced_inverse_facts(find):
        reasoning.append((depth, "%s is part of deduced inverse facts." % find))
        return False
    elif kb.part_of_deduced_undetermined_facts(find):
        reasoning.append((depth, "%s is part of deduced undetermined facts." % find))
        return None
    else:
        reasoning.append((depth, "%s is not part of initial facts." % find))
    results = list()
    final = False
    for rule in kb.associated_rules(find):
        if already_visited(rule, visited):
            pass
        reasoning.append((depth, "%s has associated rule: %s." % (find, kb.rule_to_string(rule))))
        results.clear()
        for i in range(len(rule)):
            if not is_connective(rule[i]) and i < rule.index("=>"):
                results.append(find_value(kb, rule[i], reasoning, depth + 1, visited, debug))
                if not isinstance(results[i], bool) and results[i] != None:
                    print_reasoning(reasoning)
                    print(rule)
                    print(results)
                    print("expert-system: Error: Value (%s) found is not Bool or None." % str(results[i]))
                    exit(1)
                reasoning.append((depth, "Now we know %s is %s. ( %s)" \
                            % (rule[i], results[i], \
                            kb.rule_to_string_with_answers(rule, results))))
            else:
                results.append(rule[i])
        deduce(results)
        if not isinstance(results[0], bool) and results[0] != None:
            print("expert-system: Error: End result of a value is not Bool or None.")
            exit(1)
        elif len(results) < 3:
            print("expert-system: Error: Rule end result should consist of at least 3 parts.")
            exit(1)
        elif "|" in results or "^" in results:
            reasoning.append((depth, "Rule '%s' gives %s an undetermined value (None)." % (kb.rule_to_string(rule), find)))
            final = None
        elif "!" in results:
            return add_db(kb, None if results[0] is None else not results[0], find)
        else:
            return add_db(kb, results[0],  find)
    reasoning.append((depth, "%s is not part of initial facts nor can its value be deduced from rules." % find))
    return add_db(kb, final, find)

def print_reasoning(reasoning):
    for part in reasoning:
        for _ in range(part[0]):
            print(" ", end="")
        print(part[1])

def search_answer(kb, show_reasoning, debug):
    reasoning = list()
    visited = list()
    for query in kb.iterate_queries():
        reasoning.clear()
        visited.clear()
        answer = find_value(kb, query, reasoning, 0, visited, debug)
        reasoning.append((0, "For query %s the final answer is: %s\n" % (query, answer)))
        if show_reasoning:
            print_reasoning(reasoning)
        else:
            print(reasoning[-1][1])
