from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import BaseScheduler
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
from shapely.geometry import Point
import os
import geopandas as gpd
import pandas as pd
import numpy as np
import json

class PersonAgent(GeoAgent):
    """Person Agent."""

    def __init__(
        self,
        unique_id,
        model,
        shape
    ):
        """
        Create a new person agent.
        :param unique_id:   Unique identifier for the agent
        :param model:       Model in which the agent runs
        :param shape:       Shape object for the agent
        :param agent_type:  Indicator if agent is infected ("infected", "susceptible", "recovered" or "dead")
        :param mobility_range:  Range of distance to move in one step
        """
        super().__init__(unique_id, model, shape)
        # Agent parameters
        self.state = "susceptible"
        self.mobility_range = 300
        self.recovery_rate = 0.2
        self.death_risk = 0.05
        self.init_infected = 0.2
        self.age=0,
        self.gender='',
        self.race='',
        self.hid=0,
        self.home = None,

        # Random choose if infected
        if self.random.random() < self.init_infected:
            self.state = "infected"
            self.model.counts["infected"] += 1  # Adjust initial counts
            self.model.counts["susceptible"] -= 1


    def print(self):
        print(self.unique_id, self.age, self.gender, self.race, self.hid, self.shape.x, self.shape.y)

    # def move_point(self, dx, dy):
    #     """
    #     Move a point by creating a new one
    #     :param dx:  Distance to move in x-axis
    #     :param dy:  Distance to move in y-axis
    #     """
    #     return Point(self.shape.x + dx, self.shape.y + dy)

    def move_point(self, dx, dy):
        return Point(self.shape.x + dx, self.shape.y + dy)

    def step(self):
        """Advance one step."""
        # If susceptible, check if exposed
        if self.state == "susceptible":
            neighbors = self.model.grid.get_neighbors_within_distance(
                self, self.model.exposure_distance
            )
            for neighbor in neighbors:
                if (
                    neighbor.state == "infected"
                    and self.random.random() < self.model.infection_risk
                ):
                    self.state = "infected"
                    break

        # If infected, check if it recovers or if it dies
        elif self.state == "infected":
            if self.random.random() < self.recovery_rate:
                self.state = "recovered"
            elif self.random.random() < self.death_risk:
                self.state = "dead"

        # If not dead, move
        if self.state != "dead":
            move_to = self.goto_location()
            # self.home = self.shape
            self.shape = move_to  # Reassign shape
            


        self.model.counts[self.state] += 1  # Count agent type

    def goto_location(self):
        category = self.get_category(self.age)
        if category == 'child':
            location = self.model.school_locations.sample(n=1)
        elif category == 'teen':
            location = self.model.school_locations.sample(n=1)
        elif category == 'adult':
            location = self.model.work_locations.sample(n=1)
        elif category == 'senior':
            location = self.model.community_locations.sample(n=1)
        else:
            location = self.model.locations.sample(n=1)

        if not location:
            return None
        else:
            return Point(float(location['geometry'].centroid.x), float(location['geometry'].centroid.y))

    def get_category(self, age):
        category = ""
        if age< 3:
            cateogry = 'infant'
        elif age >= 3 and age <= 12:
            category = 'child'
        elif age >= 13 and age < 19:
            category = 'teen'
        elif age >= 18 and age < 60:
            category = 'adult'
        else:
            category = 'senior'
        return category

    def __repr__(self):
        return "Person " + str(self.unique_id)


class InfectedModel(Model):
    """Model class for a simplistic infection model."""

    # Geographical parameters for desired map
    MAP_COORDS = [27.9304263, -82.307282]  # Tampa

    # geojson_regions = "Zip_Codes.geojson"
    # unique_regions = "Zip_Code"
    #
    # geojson_agents = "location_graph33612.geojson"
    # unique_agents = "id"



    def __init__(self, pop_size, init_infected, exposure_distance, infection_risk=0.2):
        """
        Create a new InfectedModel
        :param pop_size:        Size of population
        :param init_infected:   Probability of a person agent to start as infected
        :param exposure_distance:   Proximity distance between agents to be exposed to each other
        :param infection_risk:      Probability of agent to become infected, if it has been exposed to another infected
        """
        self.schedule = BaseScheduler(self)
        self.grid = GeoSpace()
        self.steps = 0
        self.counts = None
        self.reset_counts()

        #Location graph
        LG = gpd.read_file(os.path.join(os.path.dirname(os.getcwd()), 'VE', 'GIS','location_graph33612.geojson'))
        LG = LG.to_crs("EPSG:3857")

        # load people
        pop = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'SynPop', 'hillsborough_pop33612.csv'))
        # Load households
        households = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'SynPop', 'hillsborough_hh33612.csv'))

        house_locations = LG[LG['type']=='house']
        house_locations = house_locations.head(n=len(households))
        self.house_locations = house_locations
        print('houses', len(house_locations))

        self.locations = LG
        self.school_locations = LG[LG['type'] == 'schools']
        self.work_locations = LG[LG['type'] == 'workplace']
        self.community_locations = LG[LG['type'] == 'community']


        # SIR model parameters
        self.pop_size = pop_size
        self.counts["susceptible"] = pop_size
        self.exposure_distance = exposure_distance
        self.infection_risk = infection_risk

        self.running = True
        self.datacollector = DataCollector(
            {
                "infected": get_infected_count,
                "susceptible": get_susceptible_count,
                "recovered": get_recovered_count,
                "dead": get_dead_count,
            }
        )

        # Generate PersonAgent population
        AC = AgentCreator(
            PersonAgent, {"model": self}
        )



        houses = pd.concat([house_locations, households], axis=1)

        # Generate households, add agent to to each household
        for index, hrow in houses.iterrows():
            point = hrow['geometry'].centroid
            occupants = hrow['occupants']
            occupants = occupants.replace('[', '').replace(']', '')
            occupants = occupants.strip()
            occupants = occupants.replace(' ','')
            occupants = occupants.split(',')
            occupants = np.array(occupants, dtype=np.int)
            persons = pop.loc[pop['uid'].isin(occupants)]
            #     #Setup household code here
            for index, prow in persons.iterrows():
                this_person = AC.create_agent(Point(point.x, point.y), "P" + str(prow['uid']))
                this_person.age = prow['age']
                this_person.gender = prow['gender']
                this_person.race = prow['race']
                this_person.hid = hrow['hid']
                this_person.home = jsonStr = json.dumps(Point(point.x, point.y).__dict__)
                # this_person.home = Point(float(point.x), float(point.y))
                # this_person.print()

            self.grid.add_agents(this_person)
            self.schedule.add(this_person)

        self.datacollector.collect(self)

    def reset_counts(self):
        self.counts = {
            "susceptible": 0,
            "infected": 0,
            "recovered": 0,
            "dead": 0,
            "moving": 0,
        }

    def step(self):
        """Run one step of the model."""
        self.steps += 1
        self.reset_counts()
        self.schedule.step()
        self.grid._recreate_rtree()  # Recalculate spatial tree, because agents are moving

        self.datacollector.collect(self)

        # Run until no one is infected
        if self.counts["infected"] == 0:
            self.running = False


# Functions needed for datacollector
def get_infected_count(model):
    return model.counts["infected"]


def get_susceptible_count(model):
    return model.counts["susceptible"]


def get_recovered_count(model):
    return model.counts["recovered"]


def get_dead_count(model):
    return model.counts["dead"]
