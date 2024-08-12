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
    def Load(path: str) -> Dataset:
        if(IsNullOrEmpty(path)): raise Exception("Path should be provided.")
        name:str = Path(path).stem
        ds:Dataset = Dataset(name)
        tree = et.parse(path)
        root = tree.getroot()
        units:List[Unit] = []
        for eUnit in root:
            name:str = eUnit.get("name")
            desc:str = eUnit.get("desc")
            unitType:str = eUnit.get("type")
            u:Unit = Unit(name,desc,unitType,None,None)
            units.append(u)

            #CC
            eCCS = eUnit.find("CCases")
            if(eCCS):
                cCases:List[str] = []
                for eCC in eCCS:
                    val:str = eCC.get("val")
                    cCases.append(val)
                u.CorrectCases = cCases

            #ICC
            eICCS = eUnit.find("ICCases")
            if(eICCS):
                icCases: List[str] = []
                for eICC in eICCS:
                    val: str = eICC.get("val")
                    icCases.append(val)
                u.IncorrectCases = icCases

            #Constraints
            eConstraints = eUnit.find("Constraints")
            constraints:List[Constraint] = []
            if(eConstraints):
                for eCons in eConstraints:
                    valuePair:str = eCons.get("criteria")
                    name,value = valuePair.split(":")
                    constraints.append(Constraint(Criteria(name,value)))
                u.Constraints = constraints

            #Context
            eContext = eUnit.find("Context")
            if(eContext):
                data = eContext.find("Data").text.replace("\n"," ").strip() if eContext.find("Data") is not None else None
                schema = eContext.find("Schema").text.strip() if eContext.find("Schema") is not None else None
                u.Context = Context(data,schema)
        ds.Units = units
        return ds

    def Save(self, ds: Dataset, path: str):
        eUnits = et.Element('Units')  # root
        units: List[Unit] = ds.Units
        for u in units:
            eUnit = et.SubElement(eUnits, "Unit")
            eUnit.set("name", u.Name)
            eUnit.set("desc", u.Description)
            eUnit.set("type", u.UnitType.name)
            # Cases
            eCCs = et.SubElement(eUnit, "CCases")
            ccs = u.CorrectCases
            for cc in ccs:
                eCC = et.SubElement(eCCs, "CCase")
                eCC.set("val", cc)
            eICCs = et.SubElement(eUnit, "ICCases")
            iccs = u.IncorrectCases
            for icc in iccs:
                eICC = et.SubElement(eICCs, "ICCase")
                eICC.set("val", icc)

        # persist
        from xml.dom import minidom
        xmlstr = minidom.parseString(et.tostring(eUnits, encoding='utf8', method='xml')).toprettyxml(indent="   ")
        myfile = open(path, "w", errors='', encoding="utf-8")
        myfile.write(xmlstr)
        myfile.close()
        print(f"The dataset has been persisted. Path: '{path}'")



if __name__ == '__main__':
    path = Paths().GetDataset("AtomicRegexValDataset")

    # Read DS
    ds:Dataset = DatasetXmlRepository.Load(path)
    print(ds)
    print(ds.Units)