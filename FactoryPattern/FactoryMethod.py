#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as elementTree
import json


'''先用这个例子，等想到有趣的例子再来替换 ˙<>˙ '''


# 函数内嵌类使得不能直接新建实例
def json_connector(json_filepath):
    class JsonConnector:
        # 保证只有一个 data 变量
        __slots__ = ('data', )

        def __init__(self, filepath):
            self.data = dict()
            with open(filepath, mode='r', encoding='utf-8') as jsonFile:
                self.data = json.load(jsonFile)

        @property
        def parsed_data(self):
            return self.data

    return JsonConnector(json_filepath)


def xml_connector(xml_filepath):
    class XMLConnector:
        __slots__ = ('tree', )

        def __init__(self, filepath):
            self.tree = elementTree.parse(filepath)

        @property
        def parsed_data(self):
            return self.tree

    return XMLConnector(xml_filepath)


def connection_factory(filepath):
    if filepath.endswith('json'):
        connector = json_connector
    elif filepath.endswith('xml'):
        connector = xml_connector
    else:
        raise ValueError('Cannot connect to {}'.format(filepath))
    return connector(filepath)


# 进行实例化
def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filepath)
    except ValueError as ve:
        print(ve)
    return factory


def main():
    sqlite_factory = connect_to('./testFile/sqlite.sq3')
    print("just a test")

    json_factory = connect_to('./testFile/jsonExample.json')
    json_data = json_factory.parsed_data
    print(json_data)

    xml_factory = connect_to('./testFile/xmlExample.xml')
    xml_data = xml_factory.parsed_data
    print(xml_data.find('lastName').text)

if __name__ == '__main__':
    main()
