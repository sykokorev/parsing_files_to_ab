# -*- coding: utf-8 -*-

def add_widget(obj, class_name=None, name=None):
    return obj.findChild(class_name, name)


def del_row(obj_list):

    for obj in obj_list:
        while obj.rowCount() > 0:
            obj.removeRow(0)


def get_items(items, item):

    res_list = []
    for row in items:
        for key in row.keys():
            if key == item:
                res_list.append(row[key])

    return res_list


def adjust_size(objects):
    for obj in objects:
        obj.minimumSizeHint()
