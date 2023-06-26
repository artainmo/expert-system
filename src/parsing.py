class Parsing:
    def __init__(self):
        self.facts = list()
        self.rules = list()
        self.queries = list()

    def __str__(self):
        ret = "Parsing Obj:\n\nrules:\n "
        for rule in self.rules:
            for part in rule:
                ret += part + " "
            ret += "\n "
        ret += "\nfacts:\n "
        for fact in self.facts:
            ret += fact + " "
        ret += "\n\nqueries:\n "
        for query in self.queries:
            ret += query + " "
        ret += "\n"
        return ret

    def add_facts(self, facts:str):
        if facts[0] == '=':
            facts = facts[1:]
        end = min(facts.find(" "), facts.find("#"))
        self.facts = list(facts[:end])

    def add_queries(self, queries:str):
        if queries[0] == '?':
            queries = queries[1:]
        end = min(queries.find(" "), queries.find("#"))
        self.queries = list(queries[:end])

    def add_rule(self, rule:str):
        new = list()
        i = 0
        length = len(rule)
        while i < length:
            if rule[i] == '#':
                break
            elif rule[i].isspace():
                i += 1
            elif rule[i:i+3] == "<=>" or rule[i:i+3] == "<->":
                new.append("<=>")
                i += 3
            elif rule[i:i+2] == "=>" or rule[i:i+2] == "->":
                new.append("=>")
                i += 2
            else:
                new.append(rule[i])
                i += 1
        self.rules.append(new)

