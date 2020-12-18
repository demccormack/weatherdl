@staticmethod
def getMetUrl(startTime, provider, forTime, issuedTime):
    if provider == "MetVuw":
        return metVurl(startTime, forTime, issuedTime)
    elif provider == "MetService Rain":
        return metServiceRain(startTime, forTime, issuedTime)


def metVuwUrl(startTime, forTime, issuedTime):

def metServiceRain(startTime, forTime, issuedTime):
