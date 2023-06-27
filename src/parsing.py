class KnowledgeBase:
    def __init__(self):
        self.facts = list()
        self.rules = list()
        self.queries = list()

    def __str__(self):
        ret = "KnowledgeBase:\n\nrules:\n "
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

    def add_fact(self, fact:str):
        self.facts.append(fact)

    def part_of_facts(self, fact:str):
        return fact in self.facts

    def iterate_facts(self):
        for fact in self.facts:
            yield fact

    def add_queries(self, queries:str):
        if queries[0] == '?':
            queries = queries[1:]
        end = min(queries.find(" "), queries.find("#"))
        self.queries = list(queries[:end])

    def add_query(self, query:str):
        self.queries.append(query)

    def iterate_queries(self):
        for query in self.queries:
            yield query

    def add_rule(self, rule:str):
        new = list()
        if_and_only_if = 0
        i = 0
        length = len(rule)
        while i < length:
            if rule[i] == '#':
                break
            elif rule[i].isspace():
                i += 1
            elif rule[i:i+3] == "<=>" or rule[i:i+3] == "<->":
                new.append("=>")
                if_and_only_if = 1
                i += 3
            elif rule[i:i+2] == "=>" or rule[i:i+2] == "->":
                new.append("=>")
                i += 2
            else:
                new.append(rule[i])
                i += 1
        self.rules.append(new)
        if if_and_only_if:
            self.rules.append(new[:new.index("=>")].extend(new[new.index("=>"):]))

    def associated_rules(self, outcome:str):
        for rule in self.rules:
            end = 0
            for part in rule:
                if part == "=>" or part == "<==>":
                    end = 1
                elif end and part == outcome:
                    yield rule
