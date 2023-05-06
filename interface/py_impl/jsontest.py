#import json

def jsonToString(source, metric, value, handshake_filepath):
        #Receive Group, Source, and Metric by plaintext name
        suuid = None
        muuid = None
        #Find related UUIDs for both
        #Implementation v3: comb file line by line for names and find other info. based on current line number
        #handshake = json.loads(handshake_filepath)
        #handshake = open(handshake_filepath)
        with open(handshake_filepath, "r") as file:
            lines = file.readlines()
            i = 0
            for row in lines:                           #.lower()'ing all strings as a safeguard
                # if group.lower() in row.lower():        #If name found, 
                #     temp = (loop-2).split(':')                 #GUUID should be 2 lines previous.
                #     guuid = temp[1].strip(",\"")
                #     temp = (loop-3).split(':')                 #Classification should be 3 lines previous.
                #     gclass = temp[1].strip(",\"")
                if source.lower() in row.lower():     #If name found,
                    temp = lines[i+1].split(':')                 #SUUID should be on next line.
                    suuid = temp[1].strip(",\"\n ")
                elif metric.lower() in row.lower():     #If name found, 
                    temp = lines[i-1].split(':')                 #MUUID should be on previous line.
                    muuid = temp[1].strip(",\"\n ")    
                    temp = lines[i-2].split(':')                 #datatype should be 2 lines previous.
                    mdata = temp[1].strip(",\"\n ")
                    temp = lines[i-3].split(':')                 #asc should be 3 lines previous.
                    masc = temp[1].strip(",\"\n ")    
                i += 1  
        return suuid + '`' + muuid + '`' + str(value)

if __name__ == "__main__":
    print(jsonToString("Python Class Stats", "students_present", 50, "handshake.out"))
