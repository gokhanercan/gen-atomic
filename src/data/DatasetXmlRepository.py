from typing import List

import src.data.Dataset
import xml.etree.ElementTree as et


class DatasetXmlRepository(object):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def Load(self, path: str) -> src.data.Dataset.Dataset:
        pass

    def Save(self, ds: src.data.Dataset.Dataset, path: str):
        eUnits = et.Element('Units')  # root
        units: List[src.data.Dataset.Unit] = ds.Units
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
    path = "..\\..\\data\\AtomicDataset.xml"  # TODO: Create central path management.

    # region Write Initial DS
    ds = src.data.Dataset.Dataset.SampleRegexValDataset()
    DatasetXmlRepository().Save(ds, path)
    exit(0)
    # endregion

    # Read DS
    # DatasetLoader.Load("")