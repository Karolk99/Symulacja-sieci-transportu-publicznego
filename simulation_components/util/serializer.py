import networkx as nx
import yaml
from pykka import ActorRef

from simulation_components.depot import BusStop
from simulation_components.generator import LoadDistribution
from simulation_components.map import Route


class Serializer:
    # NOTE this class is a pure chaos
    #   reader discretion advised
    lines = 'lines'
    stops = 'stops'
    weights = 'weights'
    schedule = 'schedule'

    _dict: dict
    _stops: dict
    _routes: []
    _edges: []
    _graph: nx.DiGraph

    def __init__(self, path: str):
        self._stops = {}
        self._dict = {}
        self._routes = []
        self._edges = []
        self._graph = nx.DiGraph()
        self.read_from_file(path)

    def read_from_file(self, path: str) -> dict:
        with open(path, 'r', encoding='utf8') as f:
            self._dict = yaml.safe_load(f)
        return self._dict

    def get_time_base(self):
        return self._dict['time']['base']

    def get_ref_rate(self):
        return self._dict['time']['refresh_rate']

    def get_routes(self) -> [Route]:
        # get loads
        loads = {}
        for load in self._dict['loads']:
            key = list(load.keys())[0]
            loads[key] = load[key]['load']

        for line in self._dict[Serializer.lines]:
            key = list(line.keys())[0]
            line = line[key]

            stops = [stop for stop in line[Serializer.stops]]
            weights = [weight for weight in line[Serializer.weights]]
            if len(stops) != len(weights):
                raise ValueError('number of stops should equal number of weights')
            schedule = [schedule for schedule in line[Serializer.schedule]]

            if not self._stops:
                self.get_stops()
            stops = [self._stops[stop] for stop in stops]

            self._routes.append(Route.from_stops(stops, weights, schedule))
        return self._routes

    def get_stops(self):
        for load in self._dict['loads']:
            key = list(load.keys())[0]
            self._stops[key] = BusStop.start(key, LoadDistribution(load[key]['load'])).proxy()
        return self._stops

    def get_graph(self):
        edges = set()
        for route in self._routes:
            for x, y in list(zip(route.topology[:-1:], route.topology[1::])):
                edges.add((x.stop.id.get(), y.stop.id.get()))
        self._edges = list(edges)
        self._graph.add_edges_from(self._edges)
        return self._graph
