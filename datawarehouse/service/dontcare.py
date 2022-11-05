"""
QSInterpreterService Documentation:
    I. Order of Operations:
        a) Create a QSInterpreterService object
        b) Call parseUrl() to parse the url
        c) Call createTokens() to create tokens from the parsed url
        d) Call verifyTokenIntegrity() to verify the integrity of the tokens
        e) Call generateStatement() to generate a statement from the tokens
    II. Overview of Methods:
        a) parseUrl() -> void:
            - Time Complexity: O(n), where n is the length of the url.
            - Splits the url into two parts.
                1. The first part is the tablename.
                2. The second part is the query.
        b) createTokens() -> void:
            - Time Complexity: O(n^m), where n is the number of characters in the query and m is the length of the operation.
            - Splits the query into two sets of tokens.
                1. stmnt_tokens: These are non-conditional tokens.
                2. op_tokens: These are conditional tokens.
            - There must always be one more stmnt_token than op_token.
        c) verifyTokenIntegrity() -> void:
            - UNFINISHED.
            - Time Complexity: O(n^m), where n is the number of stmnt_tokens and m is the number of ILLEGALS.
            - Here we will make sure each token is valid.
            - I have also added some illegal operations that cannot be in the tokens (not sure if this is necessary).
        d) generateStatement() -> str:
            - Time Complexity: O(n), where n is the number of stmnt_tokens.
            - This method will construct a sql statement from the tokens.
            - It starts with `SELECT * FROM` and then adds the tablename.
            - Then it adds the stmnt_tokens and op_tokens.
            - For every op_token, there is a corresponding stmnt_token on the left and right of it.
            - Example:
                -> Query: 7ef719c9-59da-4262-a94b-6d9bb17c2f11?elem1__lt=n__and=elem2__gt=m
                -> Tablename: 7ef719c9-59da-4262-a94b-6d9bb17c2f11
                -> stmnt_tokens: ['elem1', 'n', 'elem2', 'm']
                -> op_tokens: ['<', 'AND', '>']
                -> Statement: SELECT * FROM 7ef719c9-59da-4262-a94b-6d9bb17c2f11 WHERE elem1 < n AND elem2 > m
            - You can also ommitt the query part of the url and it will select everything from the table.
            - However, it must contain `?`.
            - Example:
                -> Query: 7ef719c9-59da-4262-a94b-6d9bb17c2f11?
                -> Tablename: 7ef719c9-59da-4262-a94b-6d9bb17c2f11
                -> stmnt_tokens: []
                -> op_tokens: []
                -> Statement: SELECT * FROM 7ef719c9-59da-4262-a94b-6d9bb17c2f11
        e) dump() -> void:
            - Time Complexity: O(1).
            - This method will print the URL, tablename, stmnt_tokens, op_tokens, and statement.
            - It is best to call this method at the end.
"""


class QSInterpreterService:
    # To add a new operation, put it here.
    OPERATIONS = {
        "lt": "<",
        "gt": ">",
        "eq": "=",
        "limit": "LIMIT",
        "and": "AND",
    }

    # Short term solution.
    ILLEGALS = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "CREATE",
        "ALTER",
        "TRUNCATE",
        "REPLACE",
        "GRANT",
    ]

    def __init__(self, url, db_url, query=None, tablename=None):
        self.url = url
        self.tablename = tablename
        self.query = query
        self.stmnt_tokens = []
        self.op_tokens = []
        self.stmnt_tokens_sz = 0
        self.op_tokens_sz = 0
        self.statement = ""

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
        opbuf = ""
        sbuf = ""

        # I am so, so sorry.
        while i < sz:
            if i < sz - 1 and self.query[i] == "_" and self.query[i + 1] == "_":
                j = i + 2  # i + 2 to put us past the `__`
                while self.query[j] != "=":
                    opbuf += self.query[j]
                    j += 1
                self.op_tokens.append(self._determineOperation(opbuf))
                self.op_tokens_sz += 1
                i += len(opbuf) + 2  # +2 for `__`. This will put us past the operation.
                self.stmnt_tokens.append(sbuf)
                self.stmnt_tokens_sz += 1
                opbuf = ""
                sbuf = ""
                # TODO: Make sure `i` is on top of `=`.
                # If it is, we need at least 1 in the op_tokens.
            else:
                sbuf += self.query[i]
            i += 1

        if self.stmnt_tokens_sz > 0:
            self.stmnt_tokens.append(sbuf)
            self.stmnt_tokens_sz += 1

        # Currently broken.
        # if self.op_tokens_sz != self.stmnt_tokens_sz - 1:
        #     raise Exception(
        #         f"UNIMPLEMENTED: Operations size `{self.op_tokens_sz}` and statements size `{self.stmnt_tokens_sz}` are imbalanced. Operations size should be statements size - 1"
        #     )

    def verifyTokenIntegrity(self):
        # This is here just in case.
        for stok in self.stmnt_tokens:
            for illegal in self.ILLEGALS:
                if illegal in stok.upper():
                    raise Exception(
                        f"Token `{stok}` contains illegal operation `{illegal}`."
                    )
        # TODO: Verify each token to make sure they are valid.

    def generateStatement(self):
        if self.stmnt_tokens_sz == 0:
            self.statement = f"SELECT * FROM {self.tablename}"
        else:
            self.statement += (
                f'SELECT * FROM "{self.tablename}" WHERE {self.stmnt_tokens[0]}'
            )
            for i in range(1, self.stmnt_tokens_sz):
                self.statement += f" {self.op_tokens[i - 1]} {self.stmnt_tokens[i]}"
        return self.statement

    def dump(self):
        print("--- QS Interpreter Dump: ---")
        print(f"URL: {self.url}")
        print(f"TABLENAME: {self.tablename}")
        print(f"QUERY: {self.query}")
        print(f"STMT_TOKENS: {self.stmnt_tokens}")
        print(f"OP_TOKENS: {self.op_tokens}")
        print(f"STATEMENT: {self.statement}")


url = "https://www.datawarehouse.com/7ef719c9-59da-4262-a94b-6d9bb17c2f11?feet__lt=3__and=people__gt=2"
# url = "https://www.datawarehouse.com/7ef719c9-59da-4262-a94b-6d9bb17c2f11?"
dburl = "postgresql://postgres:postgres@localhost:5432/data_warehouse"
q = QSInterpreterService(url, dburl)
q.parseUrl()
q.createTokens()
q.verifyTokenIntegrity()
q.generateStatement()
q.dump()