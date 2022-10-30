class QueryStringInterpreter:
    # To add a new operation, put it here.
    OPERATIONS = {
        "lt": '<',
        "gt": '>',
        "eq": '=',
        "limit": "lim",
    }
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
        for key in self.OPERATIONS:
            if op == key:
                return self.OPERATIONS[key]
        return f"Operation `{op}` not implemented."

    def createTokens(self):
        if not self._check():
            raise Exception("No query or tablename has been given. Run _.parseUrl().")
        sz = len(self.query)
        i = 0
        j = 0
        # We could gain some speed by using arrays with a size instead of heap-allocated strings.
        opbuf = ""
        sbuf = ""
        while i < sz:
            if i < sz-1 and self.query[i] == '_' and self.query[i+1] == '_':
                # i + 2 to put us past the `__`
                j = i + 2
                while self.query[j] != '=':
                    opbuf += self.query[j]
                    j += 1
                self.op_tokens.append(self._determineOperation(opbuf))
                # +2 for `__`. This will put us past the operation.
                i += len(opbuf) + 2
                opbuf = ""
                self.stmnt_tokens.append(sbuf)
                sbuf = ""
            else:
                sbuf += self.query[i]
            i += 1
        self.stmnt_tokens.append(sbuf)

    def generateStatement(self):
        if not self._check():
            raise Exception("No query or tablename has been given. Run _.parseUrl().")

    def dump(self):
        print(f"URL: {self.url}")
        print(f"TABLENAME: {self.tablename}")
        print(f"QUERY: {self.query}")
        print(f"OP_TOKENS: {self.op_tokens}")
        print(f"STMT_TOKENS: {self.stmnt_tokens}")

qs = "https://www.datawarehouse.com/thermometertable?timestamp__lt=10pm10/30/22"
q = QueryStringInterpreter(qs, None, None)
q.parseUrl()
q.createTokens()
q.dump()



