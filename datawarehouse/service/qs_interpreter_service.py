class QueryStringInterpreter:
    def __init__(self, url, query, tablename):
        self.url = url
        self.tablename = tablename
        self.query = query
        self.stmnt_tokens = []
        self.op_tokens = []

    def parseUrl(self):
        slash_idx = -1
        question_idx = -1

        for i in range(0, len(self.url)):
            if self.url[i] == '/':
                slash_idx = i;
            if self.url[i] == '?':
                question_idx = i
                break

        self.tablename = self.url[slash_idx+1:question_idx]
        self.query = self.url[question_idx+1:]

    def _check(self):
        return not (self.query == None and self.tablename == None)

    def _determineOperation(self, op):
        if op == "lt":
            return '<'
        elif op == "gt":
            return '>'
        elif op == "eq":
            return '='
        else:
            return "op not implemented"

    def createTokens(self):
        if not self._check():
            raise Exception("No query or tablename has been given. Run _.parseUrl().")
        start = -1
        end = -1
        sz = len(self.query)
        i = 0
        j = 0
        opbuf = ""
        # sbuf = ""
        while i < sz:
            if start == -1:
                start = i
            if end != -1 or i == sz-1:
                self.stmnt_tokens.append(self.query[start:end])
                start = -1
                end = -1
            if i < sz-1 and self.query[i] == '_' and self.query[i+1] == '_':
                end = i
                j = i + 2 # i + 2 to put us past the `__`
                while self.query[j] != '=':
                    opbuf += self.query[j]
                    j += 1
                self.op_tokens.append(self._determineOperation(opbuf))
                i += len(opbuf) + 2 # +2 for `__`. This will put us past the operation.
                buf = ""
            i += 1

        print(self.stmnt_tokens)
        print(self.op_tokens)

    def generateStatement(self):
        if not self._check():
            raise Exception("No query or tablename has been given. Run _.parseUrl().")

    def dump(self):
        print(f"url = {self.url}")
        print(f"tablename = {self.tablename}")
        print(f"query = {self.query}")

qs = "https://www.datawarehouse.com/thermometertable?timestamp__lt=10pm10/30/22"
q = QueryStringInterpreter(qs, None, None)
q.parseUrl()
q.createTokens()
q.dump()



