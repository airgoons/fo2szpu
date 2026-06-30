import dcs
from unit_map import UnitMap, Formation

class Vehicle:
    def __init__(self, name:str, parent:VehicleSet, dcs_object, position:dcs.mapping.Point, is_static=True):
        self.name = name
        self.parent = parent
        self.dcs_object = dcs_object
        self.position = position
        self.is_static = is_static


class VehicleSet:
    def __init__(self, name:str, tags:list, faction:UnitMap.Faction, nation:UnitMap.Nation, formation:UnitMap.Formation, position:dcs.mapping.Point):
        self.name = name
        self.tags = tags
        self.faction = faction
        self.nation = nation
        self.formation = formation
        self.position = position
        self.positioner = VehiclePositioner(formation.zone_radius, formation.dispersion_distance)
        self.vehicles = self.positioner.generate_positions(formation)

    @staticmethod
    def sets_from_formations(formations:dict):
        sets = []

        for name, formation in formations.items():
            vehicle_set = VehicleSet(name, formation.tags, formation.nation.faction, formation.nation, formation, formation.position)
            sets.append(vehicle_set)

        return sets
        

class VehiclePositioner:
    """
    governs the positionining logic of unit_map.Formations
        zone_radius:            the maximum distance from the formation's given approximate position
        dispersion_distance:    the distance between vehicles

    """
    _STATIC_SPAWN_OVERRIDE = {
        type(dcs.vehicles.AirDefence): True
    }

    _COMBAT_VEHICLE_OVERRIDE = {
        type(dcs.vehicles.Unarmed): True
    }

    def __init__(self, zone_radius:int, dispersion_distance:int):
        self.zone_radius = zone_radius
        self.dispersion_distance = dispersion_distance
    
    def generate_positions(self, formation):
        raise NotImplementedError()
