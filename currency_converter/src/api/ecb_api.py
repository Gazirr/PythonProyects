import requests
import xml.etree.ElementTree as ET

def load_rates():
    url ="https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    response = requests.get(url)
    xml_data = response.content
    tree = ET.fromstring(xml_data)
    namespace ={"ns":"http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}
    cube_time = tree.find(".//ns:Cube/ns:Cube", namespace)
    date = cube_time.attrib["time"]
    rates = {"EUR": 1.0}
    for cube in cube_time.findall("ns:Cube", namespace):
        currency = cube.attrib["currency"]
        rate = float(cube.attrib["rate"])
        rates[currency] = rate
    return date, rates