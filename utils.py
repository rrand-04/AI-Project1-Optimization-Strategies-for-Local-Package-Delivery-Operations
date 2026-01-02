import math

#between two locations is calculated using the Euclidean distance formula
def EulideanDistance (p1,p2):
    return math.sqrt((p1[0] -p2[0] )**2 + (p1[1] - p2[1]) **2)

def TotalRouteDistance(route,start=(0,0)):

    distance=0.0
    prev=start
    for pkg in route:
        distance+= EulideanDistance(prev,pkg.destination)
        prev= pkg.destination
    distance+= EulideanDistance(prev,start)
    return distance

