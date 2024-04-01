from src.data.Dataset import Dataset, Unit, UnitType
import xml.etree.ElementTree as ET

class DatasetXmlRepository(object):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def Load(self, path:str)->Dataset:
        pass

    def Save(self,ds:Dataset, path:str):
        eUnits = ET.Element('Units')    #root
        units:[Unit] = ds.Units
        for u in units:
            eUnit = ET.SubElement(eUnits, "Unit")
            eUnit.set("name", u.Name)
            eUnit.set("desc", u.Description)
            eUnit.set("type", u.UnitType.name )
            #Cases
            eCCs = ET.SubElement(eUnit, "CCases")
            ccs = u.CorrectCases
            for cc in ccs:
                eCC = ET.SubElement(eCCs, "CCase")
                eCC.set("val",cc)
            eICCs = ET.SubElement(eUnit, "ICCases")
            iccs = u.IncorrectCases
            for icc in iccs:
                eICC = ET.SubElement(eICCs, "ICCase")
                eICC.set("val", icc)

        #persist
        from xml.dom import minidom
        xmlstr = minidom.parseString(ET.tostring(eUnits,encoding='utf8', method='xml')).toprettyxml(indent="   ")
        myfile = open(path, "w", errors='',encoding="utf-8" )
        myfile.write(xmlstr)
        myfile.close()
        print("Dataset has been persisted. Path: " + str(path))

if __name__ == '__main__':
    path = "..\\..\\data\\AtomicDataeset.csv"       #TODO: Create central path management

    #region Write Initial DS
    units = [
        Unit("Email", "email address", UnitType.RegexVal,
              ["mail@gokhanercan.com", "amojtehed@gmail.com"],
              ["dsadsadasda", "http://invalidaemail"]
              ),
        Unit("PriceInTL", "price formatted with thousands seperator in Turkish Lira currency",UnitType.RegexVal,
              ["1.550,5", "100"],
              ["090", "0,23,34", "12.11,23", "aaaa", "mail@gokhan.com"]
              )
    ]
    ds = Dataset()
    ds.Units = units
    DatasetXmlRepository().Save(ds,path)
    exit(0)
    #endregion

    #Read DS
    #DatasetLoader.Load("")