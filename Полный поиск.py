from geocoder import get_coordinates, get_ll_span
from map_api import show_map

import sys



def main():
    toponym_to_find = " ".join(sys.argv[1:])

    if toponym_to_find:
        lat, lon = get_coordinates(toponym_to_find)
        ll_spn = "ll={0},{1}&spn=0.005,0.005".format(lat, lon)
        show_map(ll_spn, "map")
        ll, spn = get_ll_span(toponym_to_find)
        ll_spn = "ll={ll}&spn={spn}".format(**locals())
        show_map(ll_spn, "map")
        point_param = "pt={ll}".format(**locals())
        show_map(ll_spn, "map", add_params=point_param)
    else:
        print('No data')


if __name__ == "__main__":
    main()
