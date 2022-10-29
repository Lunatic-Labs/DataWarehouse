class QueryStringInterpreter:
    def __init__(self, url, query=None, tablename=None):
        self.url = url
        self.tablename = tablename
        self.query = query

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

    def parseQuery(self):
        if self.query == None or self.tablename == None:
            raise Exception("No query or tablename has been given. Run _.parseUrl().")

    def dump(self):
        print(f"url = {self.url}")
        print(f"tablename = {self.tablename}")
        print(f"query = {self.query}")



qs = "https://www.datawarehouse.com/thermometertable?timestamp__lt=10pm10/30/22"
q = QueryStringInterpreter(qs)
q.parseUrl()
q.parseQuery()
q.dump()



