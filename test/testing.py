# -*- coding: utf-8 -*-

from fl_conn_builder.cflights import flight, load_flights
import unittest
import fl_conn_builder.ConnectionBuilder as Cb
from datetime import timedelta, datetime
import fl_conn_builder.flight_node as flight_node
import fl_conn_builder.graph_explorer as gexp
from fl_conn_builder.connection import connection, connectionList
from fl_conn_builder.masterData import load_airports, load_mct
from fl_conn_builder.mct_calculator import mct_calculation


class TestcFlightsMethods(unittest.TestCase):
    def test_load_fligts(self):
        data = load_flights("../data/programa_vuelo_new.csv")
        self.assertEqual(str(list(data.values())[1]),
                         "company:NT fl:102 dep:2022-05-09 08:00:00 arr:2022-05-09 08:30:00 " +
                         "orig:TFN des:LPA type: eqp:AT7 stops:0 dur:0:30:00")

    def test_flights(self):
        fl = flight("NT", "101", datetime(2016, 1, 1, hour=8),
                    datetime(2016, 1, 1, hour=9),
                    "LPA", "TFN", "J", "AT7",
                    duration=timedelta(minutes=60),
                    stops=0)

        self.assertEqual(fl.get_id(), "2016-01-01NT101LPA")


class TestcConnectionMethods(unittest.TestCase):
    def test_connectionList(self):
        fl1 = flight("NT", "101", datetime(2016, 1, 1, hour=8),
                     datetime(2016, 1, 1, hour=9),
                     "LPA", "TFN", "J", "AT7",
                     duration=timedelta(minutes=60),
                     stops=0)
        fl2 = flight("NT", "102", datetime(2016, 1, 1, hour=10),
                     datetime(2016, 1, 1, hour=11),
                     "TFN", "LPA", "J", "AT7",
                     duration=timedelta(minutes=60),
                     stops=0)

        fl3 = flight("NT", "104", datetime(2016, 1, 1, hour=11),
                     datetime(2016, 1, 1, hour=12),
                     "TFN", "LPA", "J", "AT7",
                     duration=timedelta(minutes=60),
                     stops=0)

        connect1 = connection([fl1, fl2])
        connect2 = connection([fl1, fl3])

        cl = connectionList(best_connection=False)
        cl.add(connect1)
        cl.add(connect2)

        self.assertEqual(2, len(cl.getList()))

        cbcl = connectionList(best_connection=True)
        cbcl.add(connect1)
        cbcl.add(connect2)

        self.assertEqual(1, len(cbcl.getList()))

        self.assertEqual(cbcl.getList()[0].get_duration(), connect1.get_duration())


class TestcConnectionBuilderMethods(unittest.TestCase):
    def test_node(self):
        data = flight_node.flight_node("101", datetime(2016, 1, 1, hour=8), "LPA",
                                       "id_vacio",
                                       tipo=flight_node.eNodeType.departure)
        self.assertEqual(data.get_id(), "2016-01-01T08:00:00_LPA_101_eNodeType.departure")

    def test_CB_basico(self):
        data = load_flights("../data/programa_vuelo.csv")
        gr = Cb.build_graph(data)

        self.assertEqual(gr.node_count(), 13)
        self.assertEqual(gr.edge_count(), 17)

        conexiones = gexp.connection_explorer(gr, data, best_connection=False)
        conexiones.saveCsv("../data/result/conexiones_temp.csv")
        self.assertEqual(len(conexiones.connectionList.getList()), 2)

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1)

        conexiones2.saveCsv("../data/result/conexionesCBbasico.csv")

    def test_CB(self):
        data = load_flights("../data/programa_vuelo_real.csv")
        gr = Cb.build_graph(data)

        self.assertEqual(gr.node_count(), 609)
        self.assertEqual(gr.edge_count(), 818)

        conexiones = gexp.connection_explorer(gr, data, best_connection=False)
        self.assertEqual(len(conexiones.connectionList.getList()), 11917)

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1197)
        conexiones2.saveCsv("../data/result/conexionesCB.csv")

    def test_un_vuelo(self):
        data = load_flights("../data/programa_vuelo_simple.csv")
        gr = Cb.build_graph_tipo2(data)

        self.assertEqual(gr.node_count(), 4)
        self.assertEqual(gr.edge_count(), 3)

        conexiones = gexp.connection_explorer(gr, data, best_connection=False)
        conexiones.saveCsv("../data/result/conexiones_un_vuelo.csv")
        self.assertEqual(len(conexiones.connectionList.getList()), 0)

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 0)

    def test_CB_basicoVersion2(self):
        data = load_flights("../data/programa_vuelo.csv")

        gr = Cb.build_graph_tipo2(data)

        self.assertEqual(gr.node_count(), 8)
        self.assertEqual(gr.edge_count(), 11)

        conexiones = gexp.connection_explorer(gr, data, best_connection=False)
        conexiones.saveCsv("../data/result/conexiones_CB_basicoversion2.csv")
        self.assertEqual(len(conexiones.connectionList.getList()), 2)

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1)

    def test_CB_basicoVersion2_con_MCT(self):
        data = load_flights("../data/programa_vuelo.csv")
        mct_data = load_mct("../data/mct.csv")
        airport_data = load_airports("../data/aeropuertos.csv")

        mct_calc = mct_calculation(airport_data, mct_data)

        gr = Cb.build_graph_tipo2(data, mct_calc)

        self.assertEqual(gr.node_count(), 8)
        self.assertEqual(gr.edge_count(), 11)

        conexiones = gexp.connection_explorer(gr, data, best_connection=False)
        conexiones.saveCsv("../data/result/conexiones_CB_basicoversion2.csv")
        self.assertEqual(len(conexiones.connectionList.getList()), 2)

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1)

    def test_CB_version2(self):
        data = load_flights("../data/programa_vuelo_real.csv")
        gr = Cb.build_graph_tipo2(data)

        self.assertEqual(gr.node_count(), 388)
        self.assertEqual(gr.edge_count(), 2437)

        conexiones = gexp.connection_explorer(gr, data, best_connection=False)
        self.assertEqual(len(conexiones.connectionList.getList()), 7579)

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1036)
        conexiones2.saveCsv("../data/result/conexionesCB_version2.csv")

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True, best_by_date_od=130)
        self.assertEqual(len(conexiones2.connectionList.getList()), 164)


class TestMasterData(unittest.TestCase):
    def test_airport(self):
        data = load_airports("../data/aeropuertos.csv")
        self.assertEqual(len(data), 10)
        self.assertEqual(data['LPA'].iatacode, "LPA")
        self.assertEqual(data['LPA'].country, "ES")

    def test_MCT(self):
        data = load_mct("../data/mct.csv")

        self.assertEqual(len(data), 12)
        self.assertEqual(data[1].airport, "LPA")
        self.assertEqual(data[1].cia_arrival, "NT")
        self.assertEqual(data[1].cia_departure, "NT")
        self.assertEqual(data[1].type_arrival, "D")
        self.assertEqual(data[1].type_departure, "I")
        self.assertEqual(data[1].mct, timedelta(minutes=45))

    def test_MCT_calculation(self):
        airports_m = load_airports("../data/aeropuertos.csv")
        mct_m = load_mct("../data/mct.csv")
        mct_calc = mct_calculation(airports_m, mct_m)

        fl1 = flight("NT", "101", datetime(2016, 1, 1, hour=8),
                     datetime(2016, 1, 1, hour=9),
                     "TFN", "LPA", "J", "AT7",
                     duration=timedelta(minutes=60),
                     stops=0)
        fl2 = flight("NT", "102", datetime(2016, 1, 1, hour=10),
                     datetime(2016, 1, 1, hour=11),
                     "LPA", "TFN", "J", "AT7",
                     duration=timedelta(minutes=60),
                     stops=0)

        self.assertEqual(mct_calc.get_mct(fl1, fl2), timedelta(minutes=30))


if __name__ == '__main__':
    unittest.main()
