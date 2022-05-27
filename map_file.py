
def get_net(tag: int):
    if tag == 2: # 2x2 grid
        net_file = 'sumo-rl/nets/2x2grid/2x2.net.xml'
    elif tag == 4: # 4x4 grid
        net_file = 'sumo-rl/nets/4x4-Lucas/4x4.net.xml'
    else:
        raise ValueError(f"invalid tag: {tag}")
    return net_file

def get_rou(tag: int):
    if tag == 2: # 2x2 grid
        rou_file = 'sumo-rl/nets/2x2grid/2x2.rou.xml'
    elif tag == 4: # 4x4 grid
        rou_file = 'sumo-rl/nets/4x4-Lucas/4x4c1c2c1c2.rou.xml'
    else:
        raise ValueError(f"invalid tag: {tag}")
    return rou_file

def get_map(tag: int):
    return get_net(tag), get_rou(tag)

    #net_file='sumo-rl/nets/RESCO/ingolstadt21/ingolstadt21.net.xml',
    #route_file='sumo-rl/nets/RESCO/ingolstadt21/ingolstadt21.rou.xml',
    #net_file='sumo-rl/nets/RESCO/cologne8/cologne8.net.xml',
    #route_file='sumo-rl/nets/RESCO/cologne8/cologne8.rou.xml',
    #net_file='sumo-rl/nets/double/network.net.xml',
    #route_file='sumo-rl/nets/double/flow.rou.xml',
    #net_file='sumo-rl/nets/RESCO/arterial4x4/arterial4x4.net.xml',
    #route_file='sumo-rl/nets/RESCO/arterial4x4/arterial4x4_1.rou.xml',
    #net_file='sumo-rl/nets/4x4-Lucas/4x4.net.xml',
    #route_file='sumo-rl/nets/4x4-Lucas/4x4c1c2c1c2.rou.xml',
    #net_file='maps/osm.net.xml',
    #route_file='maps/osm.passenger.trips.xml',

def out_folder(tag: int): # out_file folder
    if tag == 2: # 2x2 grid
        out_file = 'outputs/2x2/'
    elif tag == 4: # 4x4 grid
        out_file = 'outpus/4x4/'
    else:
        raise ValueError(f"invalid tag: {tag}")
    return out_file