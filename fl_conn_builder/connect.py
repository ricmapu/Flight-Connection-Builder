# -*- coding: utf-8 -*-
import argparse
from mct_calculator import mct_calculation

from cflights import load_flights
import ConnectionBuilder as Cb
import graph_explorer as gexp
from masterData import load_airports, load_mct
from datetime import timedelta, datetime


def main():
    parser = argparse.ArgumentParser(description='Flight connection builder')

    parser.add_argument('schedule', metavar='schedule', help='flight program file')
    parser.add_argument('connections', metavar='result', help='Connection file')

    parser.add_argument('--mct', dest="mct_file", help='MCT file')
    parser.add_argument('--airport', dest="airport_file", help='airports file')
    parser.add_argument('--connection', choices=['all', 'best_OD', 'best_flight'], default='all')
    parser.add_argument('--max_connection', metavar="max_connect",
                        type=int, default=6)

    args = parser.parse_args()

    print("loading data ...", end='')

    start = datetime.now()
    flight_data = load_flights(args.schedule)
    mct_data = load_mct(args.mct_file)
    airport_data = load_airports(args.airport_file)
    mct_calc = mct_calculation(airport_data, mct_data)
    end = datetime.now()

    print(end - start)

    print("creating graph ...", end='')

    start = datetime.now()
    gr = Cb.build_graph_tipo2(flight_data, mct_calc,
                              max_connect_time=timedelta(hours=args.max_connection))
    end = datetime.now()
    print(end - start)

    print("exploring graph ...", end='')
    start = datetime.now()

    if args.connection == "all":
        best_connection = False
        best_by_date_od = False
    elif args.connection == "best_OD":
        best_connection = True
        best_by_date_od = True
    elif args.connection == "best_flight":
        best_connection = True
        best_by_date_od = False

    conexiones = gexp.connection_explorer(gr, flight_data, best_connection, best_by_date_od)
    end = datetime.now()
    print(end - start)

    print("saving graph ...", end='')
    start = datetime.now()
    conexiones.saveCsv(args.connections)
    end = datetime.now()
    print(end - start)


if __name__ == "__main__":
    main()
