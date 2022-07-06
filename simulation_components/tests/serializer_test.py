import unittest
import pykka
from simulation_components.depot import BusStop
from simulation_components.generator import LoadDistribution
from simulation_components.map import Route
from simulation_components.util.serializer import Serializer


class TestSerializer(unittest.TestCase):
    def test_basic_parse(self):
        example_config = {'time': {'base': 24},
                          'lines': [{
                              'line01': {
                                  'name': 'line01',
                                  'stops': ['A', 'B', 'C'],
                                  'weights': [10, 10, 20],
                                  'schedule': ['10:10', '15:10', '16:10', '18:10', '20:10']}}
                          ]}

        result = Serializer.read_from_file('./example_config.yaml')
        self.assertEqual(result, example_config)

    def test_basic_parse_to_route(self):
        result = Serializer.get_routes('./example_config.yaml')
        load = LoadDistribution([1] * 24)
        schedule = ['10:10', '15:10', '16:10', '18:10', '20:10']
        weights = [10, 10, 20]

        stops = [BusStop.start(stop, load).proxy() for stop in ['A', 'B', 'C']]

        route = Route.from_stops(stops, weights, schedule)
        self.assertEqual(route.schedule, result[0].schedule)
        for t1, t2 in zip(route.topology, result[0].topology):
            self.assertEqual(t1.to_next, t2.to_next)
            self.assertEqual(t1.stop.load_distribution.get(),
                             t2.stop.load_distribution.get())

    @classmethod
    def tearDownClass(cls) -> None:
        pykka.ActorRegistry.stop_all()
