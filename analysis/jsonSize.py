import json
import os
import sys

dict = {}

for a in range(0, 720):
    dict[a] = {'time': '2021-12-01-12:00:00',
    "i_temp":00.00,
    "i_hum":00.00,
    "o_temp":00.00,
    "o_hum":00.00,
    "o_wind":00.00,
    "o_rain":00.00
    }

output = json.dumps(dict, indent = 4)   

print ("Estimated size: " + str(sys.getsizeof(output) / 1024) + "KB")