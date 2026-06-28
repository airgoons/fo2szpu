import os
import json
from operator import attrgetter
from enum import StrEnum, auto

import dcs


class UnitSetEntry:
    def __init__(self, dcs_obj_name:str, qty:int):
        self.dcs_obj_name = dcs_obj_name
        self.qty = qty

        try:
            self.dcs_obj = attrgetter(dcs_obj_name)(dcs)
        except:
            raise RuntimeError("Invalid DCS object name [{0}]".format(dcs_obj_name))

    @staticmethod
    def from_dict(d):
        return UnitSetEntry(
            dcs_obj_name = d["dcs_obj_name"],
            qty = d["qty"]
        )


class Formation:
    class FormationType(StrEnum):
        ADA = "ADA"
        ARMOR = "ARMOR"
        ARTY = "ARTY"
        ENG = "ENG"
        GUER = "GUER"
        HQ = "HQ"
        INF = "INF"
        LAT = "LAT"
        MECH = "MECH"
        MLRS = "MLRS"
        SF = "SF"
        
    def __init__(self, formation_type:FormationType, spawn_radius:int, unit_set:list):
        self.formation_type = formation_type
        self.spawn_radius = spawn_radius
        self.unit_set = unit_set

    @staticmethod
    def from_dict(key, data):
        unit_set_raw = [UnitSetEntry.from_dict(entry) for entry in data["unit_set"]]
        
        unit_set = []
        for entry in unit_set_raw:
            unit_set.extend([entry.dcs_obj] * entry.qty)

        return Formation(
            formation_type = Formation.FormationType(key),
            spawn_radius = data["spawn_radius"],
            unit_set = unit_set   
        )


class Nation:
    def __init__(self, tag:str, formations:dict):
        self.tag = tag
        self.formations = formations

    @staticmethod
    def from_dict(key, data):
        return Nation(
            tag = key,
            formations = {
                formation.formation_type: formation for formation in
                (Formation.from_dict(k, v) for k,v in data.items())
            }
        )


class Faction:
    def __init__(self, tag:str, unit_heading:int, nations:list):
        self.tag = tag
        self.unit_heading = unit_heading
        self.nations = nations

    @staticmethod
    def from_dict(key, data):
        return Faction(
            tag = key,
            unit_heading = data["unit_heading"],
            nations = {
                nation.tag: nation for nation in
                (Nation.from_dict(k, v) for k,v in data["nations"].items())
            }
        )


class UnitMap:
    def __init__(self, miz_drawing_layer:str, factions:dict):
        self.miz_drawing_layer = miz_drawing_layer
        self.factions = factions

    @staticmethod
    def from_dict(data):
        return UnitMap(
            miz_drawing_layer = data["miz_drawing_layer"],
            factions = {
                faction.tag: faction for faction in
                (Faction.from_dict(k, v) for k,v in data["factions"].items())
            }
        )

    @staticmethod
    def from_json(path):
        """Imports unit mapping data from a json"""
        # Input Validation
        path = os.path.abspath(path)
        if not os.path.isfile(path):
            raise RuntimeError(f"Path does not exist or is not a file [{path}]")

        data = None
        try:
            with open(path, 'r') as json_file:
                data = json.load(json_file)
        except Exception as e:
            raise RuntimeError(f"JSON load failure [{path}]") from e

        return UnitMap.from_dict(data)
