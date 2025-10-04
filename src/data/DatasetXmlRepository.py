from typing import List
from pathlib import Path

import xml.etree.ElementTree as et

from data.Dataset import Dataset, Unit, Constraint, Criteria, Context
from utility.Paths import Paths
from utility.StringHelper import IsNullOrEmpty


class DatasetXmlRepository(object):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def load(path: str) -> Dataset:
        if IsNullOrEmpty(path):
            raise Exception("Path should be provided.")
        name: str = Path(path).stem
        ds: Dataset = Dataset(name)
        tree = et.parse(path)
        root = tree.getroot()
        units: List[Unit] = []
        for e_unit in root:
            name: str = e_unit.get("name")
            desc: str = e_unit.get("desc")
            unit_type: str = e_unit.get("type")
            u: Unit = Unit(name, desc, unit_type, None, None)
            units.append(u)

            # CC
            e_ccs = e_unit.find("CCases")
            if e_ccs:
                c_cases: List[str] = []
                for e_cc in e_ccs:
                    val: str = e_cc.get("val")
                    c_cases.append(val)
                u.correct_cases = c_cases

            # ICC
            e_iccs = e_unit.find("ICCases")
            if e_iccs:
                ic_cases: List[str] = []
                for e_icc in e_iccs:
                    val: str = e_icc.get("val")
                    ic_cases.append(val)
                u.incorrect_cases = ic_cases

            # Constraints
            e_constraints = e_unit.find("Constraints")
            constraints: List[Constraint] = []
            if e_constraints:
                for e_cons in e_constraints:
                    value_pair: str = e_cons.get("criteria")
                    name, value = value_pair.split(":")
                    constraints.append(Constraint(Criteria(name, value)))
                u.constraints = constraints

            # Context
            e_context = e_unit.find("Context")
            if e_context:
                data = (
                    e_context.find("Data").text.replace("\n", " ").strip() if e_context.find("Data") is not None else None
                )
                schema = e_context.find("Schema").text.strip() if e_context.find("Schema") is not None else None
                u.context = Context(data, schema)
        ds.units = units
        return ds

    def save(self, ds: Dataset, path: str):
        e_units = et.Element("Units")  # root
        units: List[Unit] = ds.units
        for u in units:
            e_unit = et.SubElement(e_units, "Unit")
            e_unit.set("name", u.name)
            e_unit.set("desc", u.description)
            e_unit.set("type", u.unit_type)
            # Cases
            e_ccs = et.SubElement(e_unit, "CCases")
            ccs = u.correct_cases
            for cc in ccs:
                e_cc = et.SubElement(e_ccs, "CCase")
                e_cc.set("val", cc)
            e_iccs = et.SubElement(e_unit, "ICCases")
            iccs = u.incorrect_cases
            for icc in iccs:
                e_icc = et.SubElement(e_iccs, "ICCase")
                e_icc.set("val", icc)

        # persist
        from xml.dom import minidom

        xmlstr = minidom.parseString(et.tostring(e_units, encoding="utf8", method="xml")).toprettyxml(indent="   ")
        myfile = open(path, "w", errors="", encoding="utf-8")
        myfile.write(xmlstr)
        myfile.close()
        print(f"The dataset has been persisted. Path: '{path}'")


if __name__ == "__main__":
    path = Paths().GetDataset("AtomicRegexValDataset")

    # Read DS
    ds: Dataset = DatasetXmlRepository.load(path)
    print(ds)
    print(ds.units)
