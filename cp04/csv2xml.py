import lxml.etree as ET
import pandas as pd
import sys , os

sys.path.append('../')
from cp03.merge_csv  import csv_reader, get_FileSize

def ticket_csv2xml(filename, header):
    """header is a header data dict."""
    # https://stackoverflow.com/questions/863183/python-adding-namespaces-in-lxml
    # xsi是常见的namespace, 无需单独指定. 对标签属性使用namespace标注后，方可不生成额外的前缀。
    NS = 'http://www.w3.org/2001/XMLSchema-instance'
    location_attribute = '{%s}noNameSpaceSchemaLocation' % NS

    TicketFile = ET.Element("TicketFile", attrib={location_attribute: 'TicketFileFormat.xsd'})

    FileHeader = ET.SubElement(TicketFile, "FileHeader")
    for k,v in header.items():
        i = ET.SubElement(FileHeader, k )
        i.text = str(v)

    Measurements = ET.SubElement(TicketFile, "Measurements")
    ObjectType =  ET.SubElement(Measurements, "ObjectType")
    ObjectType.text = 'Ticket'

    TicketName =  ET.SubElement(Measurements, "TicketName")
    csv_rows = csv_reader(filename)
    for k,v in enumerate(csv_rows[0] , 1) :
        i = ET.SubElement(TicketName, "N" )
        i.set("i", str(k))
        i.text = v

    TicketData = ET.SubElement(Measurements, "TicketData")
    for k,v in enumerate(csv_rows[1:] , 1) :
        Ticket = ET.SubElement(TicketData, "Ticket" )
        Ticket.set("Id", str(k))
        for l, w in enumerate(v , 1) :
            i = ET.SubElement(Ticket, "V" )
            i.set("i", str(l) )
            i.text = w

    filename_xml = os.path.splitext(filename)[0]+".xml"
    ET.ElementTree(TicketFile).write(filename_xml, encoding='UTF-8', xml_declaration=True, method='xml', pretty_print = True)
    print("To XML_File:{}, Size:{}".format(filename_xml, get_FileSize(filename_xml)))

    return ET.tostring(TicketFile, encoding='UTF-8', xml_declaration=True, method='xml', pretty_print = True)

if __name__ == '__main__':
    fileheader = pd.read_excel("./CP4- header 规划.xlsx",index_col="文件名").to_dict("index")
    for k,v in fileheader.items() :
        if os.path.isfile(k):
            print("CSV File:{}, Size:{}".format(k, get_FileSize(k)))
            ticket_csv2xml(k,v)

# python csv2xml.py
# CSV File:QLR2019020710-001.csv, Size:0.18
# To XML_File:QLR2019020710-001.xml, Size:1.29
# CSV File:QLR2019020710-002.csv, Size:0.18
# To XML_File:QLR2019020710-002.xml, Size:1.3
# CSV File:QLR2019020710-003.csv, Size:0.18
# To XML_File:QLR2019020710-003.xml, Size:1.29
