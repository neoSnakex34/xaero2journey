import json

#removes deahtpoint for every dimension file in xaeros, can be changed to mantain them, i just don't really use them
#and find kinda frustrating having my map crowded with deathpoints 
def file_cleaner():
    waypoints = []
    for dim in range(-1,2):
        #open waypoint file in dimension folder (YOU HAVE TO MANUALLY COPY the file from dim%n in each new folder)
        #note that if filename is different you have to change it
        with open(str(dim)+'/mw1,1,1_1.txt', encoding='utf8') as f:
            a = f.readlines()[3:]
        waypoints.extend([w[:-1]+':'+str(dim) for w in a if not w.startswith("waypoint:gui.xaero_deathpoint")])
    return waypoints

def journey_converter(waypoints):
    for waypoint in waypoints:
        xaero2journey(waypoint)

#   0       1        2  3     4  5    6  7     8  9                10    11 12 13
# waypoint:villaggo2:V:-1853:91:-9219:12:false:0:gui.xaero_default:false:0:0:false:-1
def xaero2journey(waypoint):

    raw = waypoint.split(':')
    
    name = raw[1]
    if '?' in name:
        name = name.replace('?', ' dubbio')
    x = raw[3]
    y = raw[4]
    z = raw[5]
    id = name+'_'+x+y+z
    dimension = raw[14]

    if dimension == '-1':
        dim = 'minecraft:the_nether'
        x = int(x) * 8
        z = int(z) * 8
    elif dimension == '0':
        dim = 'minecraft:overworld'
    elif dimension == '1':
        dim = 'minecraft:the_end'
    else:
        print('error in parsing dimension, aborting')

    journey_obj = {
        
        "id": id,
        "name": name,
        "icon": "journeymap:ui/img/waypoint-icon.png",
        "colorizedIcon": "fake:color--3610774-waypoint-icon.png",
        "x": int(x),
        "y": int(y),
        "z": int(z),
        #color can be adjusted here and even infered from xaeros data
        #i just don't care a lot about it and you can still modify your waypoint 
        #once imported in journey
        "r": 100,
        "g": 100,
        "b": 255,
        "enable": True,
        "type": "Normal",
        "origin": "journeymap",
        "dimensions": [
            dim
        ],
        "persistent": True,
        "showDeviation": False,
        "iconColor": -1,
        "customIconColor": False,

    }
    json_obj = json.dumps(journey_obj, indent=2)
    
    #be sure to have converted folder in executing path, and empty it if it not
    with open('converted/'+id+'.json', 'w+') as f:
        f.write(json_obj)

if __name__ == '__main__':
    way = file_cleaner()
    journey_converter(way)