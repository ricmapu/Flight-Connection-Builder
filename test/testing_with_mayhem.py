import unittest
import datetime
from datetime import timedelta
from core.task import Task
from core.DayWeekDay import DayWeekDay
from util.ssimReader import SSIMReader

from fl_conn_builder.connection import connection, connectionList
import fl_conn_builder.ConnectionBuilder as Cb
import fl_conn_builder.graph_explorer as gexp
from fl_conn_builder.mct_calculator import mct_calculation
from fl_conn_builder.masterData import load_airports, load_mct


class TestConnectionMethods(unittest.TestCase):
    def test_connectionList(self):
        fl1 = Task(departure=DayWeekDay(a_date=datetime.datetime(2016, 1, 1), a_time=datetime.time(8, 0, 0)),
                   origin="LPA", destination="TFN", task_number="101",
                   duration=timedelta(minutes=30))

        fl2 = Task(departure=DayWeekDay(a_date=datetime.datetime(2016, 1, 1), a_time=datetime.time(10, 0, 0)),
                   origin="TFN", destination="LPA", task_number="102",
                   duration=timedelta(minutes=30))

        fl3 = Task(departure=DayWeekDay(a_date=datetime.datetime(2016, 1, 1), a_time=datetime.time(11, 0, 0)),
                   origin="TFN", destination="LPA", task_number="104",
                   duration=timedelta(minutes=60))

        connect1 = connection([fl1, fl2])
        connect2 = connection([fl1, fl3])

        cl = connectionList(best_connection=False)
        cl.add(connect1)
        cl.add(connect2)

        self.assertEqual(2, len(cl.getList()))

        connection_list = connectionList(best_connection=True)
        connection_list.add(connect1)
        connection_list.add(connect2)

        self.assertEqual(1, len(connection_list.getList()))

        self.assertEqual(connection_list.getList()[0].get_duration(), connect1.get_duration())


class TestConnectionBuilderMethods(unittest.TestCase):
    def test_CB_basico(self):
        reader = SSIMReader()

        file_name = "../data/programa_vuelo_ssim.txt"
        sched = reader.read(file_name)

        gr = Cb.build_graph(sched)

        self.assertEqual(gr.node_count(), 14)
        self.assertEqual(gr.edge_count(), 18)

        conexiones = gexp.connection_explorer(gr, sched, best_connection=False)
        conexiones.saveCsv("../data/result/conexiones_temp.csv")
        self.assertEqual(len(conexiones.connectionList.getList()), 1)

        conexiones2 = gexp.connection_explorer(gr, sched, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1)

        conexiones2.saveCsv("../data/result/conexionesCBbasico.csv")

    def test_CB(self):
        reader = SSIMReader()

        file_name = "../data/programa_vuelo_real_ssim.txt"
        sched = reader.read(file_name)

        gr = Cb.build_graph(sched)

        self.assertEqual(gr.node_count(), 609)
        self.assertEqual(gr.edge_count(), 818)

        conexiones = gexp.connection_explorer(gr, sched, best_connection=False)
        self.assertEqual(len(conexiones.connectionList.getList()), 11917)

        conexiones2 = gexp.connection_explorer(gr, sched, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1197)
        conexiones2.saveCsv("../data/result/conexionesCB.csv")

    def test_un_vuelo(self):
        reader = SSIMReader()

        file_name = "../data/programa_vuelo_simple_ssim.txt"
        sched = reader.read(file_name)
        gr = Cb.build_graph_tipo2(sched)

        self.assertEqual(gr.node_count(), 4)
        self.assertEqual(gr.edge_count(), 3)

        conexiones = gexp.connection_explorer(gr, sched, best_connection=False)
        conexiones.saveCsv("../data/result/conexiones_un_vuelo.csv")
        self.assertEqual(len(conexiones.connectionList.getList()), 0)

        conexiones2 = gexp.connection_explorer(gr, sched, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 0)

    def test_CB_basicoVersion2(self):
        reader = SSIMReader()

        file_name = "../data/programa_vuelo_ssim.txt"
        sched = reader.read(file_name)

        gr = Cb.build_graph_tipo2(sched)

        self.assertEqual(gr.node_count(), 8)
        self.assertEqual(gr.edge_count(), 10)

        conexiones = gexp.connection_explorer(gr, sched, best_connection=False)
        conexiones.saveCsv("../data/result/conexiones_CB_basicoversion2.csv")
        self.assertEqual(len(conexiones.connectionList.getList()), 1)

        conexiones2 = gexp.connection_explorer(gr, sched, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1)

    def test_CB_basicoVersion2_con_MCT(self):
        reader = SSIMReader()
        file_name = "../data/programa_vuelo_ssim.txt"
        data = reader.read(file_name)

        mct_data = load_mct("../data/mct.csv")
        airport_data = load_airports("../data/aeropuertos.csv")

        mct_calc = mct_calculation(airport_data, mct_data)

        gr = Cb.build_graph_tipo2(data, mct_calc)

        self.assertEqual(gr.node_count(), 8)
        self.assertEqual(gr.edge_count(), 10)

        conexiones = gexp.connection_explorer(gr, data, best_connection=False)
        conexiones.saveCsv("../data/result/conexiones_CB_basicoversion2.csv")
        self.assertEqual(len(conexiones.connectionList.getList()), 1)

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1)

    def test_CB_version2(self):
        reader = SSIMReader()
        file_name = "../data/programa_vuelo_real_ssim.txt"
        data = reader.read(file_name)

        gr = Cb.build_graph_tipo2(data)

        self.assertEqual(gr.node_count(), 388)
        self.assertEqual(gr.edge_count(), 2437)

        conexiones = gexp.connection_explorer(gr, data, best_connection=False)
        self.assertEqual(len(conexiones.connectionList.getList()), 7579)

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 1036)
        conexiones2.saveCsv("../data/result/conexionesCB_version2.csv")

        conexiones2 = gexp.connection_explorer(gr, data, best_connection=True, best_by_date_od=True)
        self.assertEqual(len(conexiones2.connectionList.getList()), 164)
        conexiones2.saveCsv("../data/result/conexionesCB_version3.csv")



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

        fl1 = Task(departure=DayWeekDay(a_date=datetime.datetime(2016, 1, 1), a_time=datetime.time(9, 0, 0)),
                   origin="LPA", destination="TFN", task_number="101",
                   duration=timedelta(minutes=30))

        fl1.set_attribute("airline_designator", "NT")

        fl2 = Task(departure=DayWeekDay(a_date=datetime.datetime(2016, 1, 1), a_time=datetime.time(10, 0, 0)),
                   origin="TFN", destination="LPA", task_number="102",
                   duration=timedelta(minutes=30))

        fl2.set_attribute("airline_designator", "NT")

        self.assertEqual(mct_calc.get_mct(fl1, fl2), timedelta(minutes=30))


if __name__ == '__main__':
    unittest.main()
