from itertools import chain

layers_left = [
    (0, -1, 'layer_1'),
    (-1, -3, 'layer_2'),
    (-3, -5, 'layer_3'),
    (-5, -7, 'layer_4')
]

layers_right = [
    (-1, -2, 'layer_5'),
    (-2, -5, 'layer_6'),
    (-5, -6, 'layer_7')
]

def combine_layers(layers_left, layers_right, xleft, xmid, xright):
    result = []
    z_combined = sorted(list(set(chain(*[[l[0], l[1]] for l in layers_left + layers_right]))), reverse=True)

    for layer in layers_left:
        coords = []
        coords.append((xleft, layer[1])) # bottomleft
        coords.append((xleft, layer[0])) # topleft
        coords.append((xmid, layer[0])) # topright
        
        z_extras = [z for z in z_combined if z < layer[0] and z > layer[1]]
        for z in z_extras:
            coords.append((xmid, z))

        coords.append((xmid, layer[1])) # bottomright    
        result.append((layer[2], coords))    

    for layer in layers_right:
        coords = []
        coords.append((xmid, layer[1])) # bottomleft

        z_extras = [z for z in z_combined if z < layer[0] and z > layer[1]]
        for z in reversed(z_extras):
            coords.append((xmid, z))

        coords.append((xmid, layer[0])) # topleft
        coords.append((xright, layer[0])) # topright
        coords.append((xright, layer[1])) # bottomright
        result.append((layer[2], coords))    

    return result

combined_layers = combine_layers(layers_left, layers_right, 0, 30, 50)
print(combined_layers)