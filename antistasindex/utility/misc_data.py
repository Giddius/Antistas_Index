

SGF = 1024  # SIZE_GENERAL_FACTOR
SIZE_CONV = {'byte': {'factor': SGF**0, 'short_name': 'b'},
             'kilobyte': {'factor': SGF**1, 'short_name': 'kb'},
             'megabyte': {'factor': SGF**2, 'short_name': 'mb'},
             'gigabyte': {'factor': SGF**3, 'short_name': 'gb'},
             'terrabyte': {'factor': SGF**4, 'short_name': 'tb'}}
