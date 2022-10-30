import sqlalchemy
class QueryStringInterpreter:
    # To add a new operation, put it here.
    OPERATIONS = {
        "lt": "<",
        "gt": ">",
        "eq": "=",
        "limit": "lim",
        "and": "AND"
    }

    def __init__(self, url, db_url, query=None, tablename=None):
        self.url = url
        self.tablename = tablename
        self.query = query
        self.stmnt_tokens = []
        self.op_tokens = []
        self.statement = ""
        self.engine = sqlalchemy.create_engine(db_url)
        self.connection = self.engine.connect()


    def parseUrl(self):
        slash_idx = -1
        question_idx = -1
        for i in range(0, len(self.url)):
            if self.url[i] == "/":
                slash_idx = i
            if self.url[i] == "?":
                question_idx = i
                break
        self.tablename = self.url[slash_idx + 1 : question_idx]
        self.query = self.url[question_idx + 1 :]

    def _determineOperation(self, op):
        for key in self.OPERATIONS:
            if op == key:
                return self.OPERATIONS[key]
        return f"Operation `{op}` not implemented."

    def createTokens(self):
        if self.query == None:
            raise Exception("No query has been given. Run _.parseUrl().")
        sz = len(self.query)
        i = 0
        j = 0
        # We could gain some speed by using arrays with a size instead of heap-allocated strings.
        opbuf = ""
        sbuf = ""
        while i < sz:
            if i < sz - 1 and self.query[i] == "_" and self.query[i + 1] == "_":
                # i + 2 to put us past the `__`
                j = i + 2
                while self.query[j] != "=":
                    opbuf += self.query[j]
                    j += 1
                self.op_tokens.append(self._determineOperation(opbuf))
                # +2 for `__`. This will put us past the operation.
                i += len(opbuf) + 2
                self.stmnt_tokens.append(sbuf)
                opbuf = ""
                sbuf = ""
                # TODO: Make sure `i` is on top of `=`.
                # If it is, we need at least 1 in the op_tokens.
            else:
                sbuf += self.query[i]
            i += 1
        self.stmnt_tokens.append(sbuf)
        op_sz = len(self.op_tokens)
        stmnt_sz = len(self.stmnt_tokens)
        if op_sz != stmnt_sz - 1:
            raise Exception(
                f"UNIMPLEMENTED: Operations size `{op_sz}` and statements size `{stmnt_sz}` are imbalanced. Operations size should be statements size - 1"
            )

    def verifyTokenIntegrity(self):
        # TODO: Verify each token to make sure they are valid.
        table = sqlalchemy.Table(self.tablename, sqlalchemy.MetaData(), autoload=True, autoload_with=self.engine)
        pass


    def generateStatement(self):
        # for i in range(0, len(self.stmnt_tokens)):
        #     if i == 0:
        #         self.stmnt_tokens[i] = f"SELECT * FROM {self.tablename} WHERE {self.stmnt_tokens[i]}"
        #     else:
        #         self.stmnt_tokens[i] = f"{self.op_tokens[i - 1]} {self.stmnt_tokens[i]}"
        # return a sqlalchemy query object
        for i in range(0, len(self.stmnt_tokens)):
            if i == 0:
                self.statement += f"SELECT * FROM \"{self.tablename}\" WHERE {self.stmnt_tokens[i]}"
            else:
                self.statement += f" {self.op_tokens[i - 1]} {self.stmnt_tokens[i]}"
        return self.statement

    def dump(self):
        print(f"URL: {self.url}")
        print(f"TABLENAME: {self.tablename}")
        print(f"QUERY: {self.query}")
        print(f"STMT_TOKENS: {self.stmnt_tokens}")
        print(f"OP_TOKENS: {self.op_tokens}")
        print(f"STATEMENT: {self.statement}")


url = "https://www.datawarehouse.com/7ef719c9-59da-4262-a94b-6d9bb17c2f11?feet__lt=3__and=beds__gt=2"
dburl = "postgresql://zdh:silverfish@localhost:5432/data_warehouse"
q = QueryStringInterpreter(url, dburl)
q.parseUrl()
q.createTokens()
q.generateStatement()
q.dump()