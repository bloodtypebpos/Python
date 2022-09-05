import sqlite3
import os
from airtable import Airtable


class Project:
    def __init__(self, base_key, api_key, conn, table, sonum):
        self.base_key = base_key
        self.api_key = api_key
        self.conn = conn
        self.sonum = sonum
        self.c = conn.cursor()
        self.table = table
        if self.sonum == "NA":
            query = 'SELECT * FROM "' + table + '"'
        else:
            query = 'SELECT * FROM "' + table + '" WHERE "Reference No" = "' + sonum + '"'
        self.rows = self.get_rows(query)
        query = 'PRAGMA table_info("' + table + '")'
        self.columns = self.get_rows(query)
        self.fields = []
        for column in self.columns:
            self.fields.append(column[1])
        if self.sonum == "NA":
            query = 'SELECT id FROM "' + table + '"'
        else:
            query = 'SELECT id FROM "' + table + '" WHERE "Reference No" = "' + sonum + '"'
        self.ids = []
        for id in self.get_rows(query):
            self.ids.append(id[0])
        query = 'SELECT '
        for field in self.fields:
            query = query + '"' + field + '",'
        if self.sonum == "NA":
            query = query[:-1] + ' FROM "' + table + '"'
        else:
            query = query[:-1] + ' FROM "' + table + '" WHERE "Reference No" IS "' + sonum + '"'
        rows = self.get_rows(query)
        self.items = self.get_items(rows)
        query = 'SELECT DISTINCT Code FROM "' + table + '"'
        self.codes = self.get_rows(query)
        self.code_items = []
        self.completed_code_items = []
        for code in self.codes:
            rows, complete_rows = self.get_codes(self.items, code[0])
            self.code_items.append(rows)
            self.completed_code_items.append(complete_rows)
        query = 'SELECT DISTINCT Customer FROM "' + table + '"'
        rows = self.get_rows(query)
        self.customer = rows[0][0]
        self.image_url = "NA"
        if self.sonum == "NA":
            pass
        else:
            query = 'SELECT Attachments FROM "' + table + '" WHERE "Reference No" = "' + sonum + '" AND "Code" = "Image"'
            rows = self.get_rows(query)
            self.image_url = rows[0][0]

    def get_rows(self, query):
        rows = []
        crows = self.c.execute(query)
        for row in crows:
            rows.append(row)
        return rows

    def get_items(self, rows):
        items = []
        for row in self.rows:
            item = Item()
            item.make_attrs(self.fields, row)
            items.append(item)
        return items

    def get_codes(self, items, code):
        rows = []
        complete_rows = []
        for item in items:
            if item.Code == code:
                rows.append(item)
                if str(item.Complete) == "1":
                    complete_rows.append(item)
        return rows, complete_rows


class Item:
    def __init__(self):
        self.test = 'Hello World'

    def update_property(self, property, value):
       setattr(self, property, value)

    def make_attrs(self, arr1, arr2):
        for i in range(0, len(arr1)):
            self.update_property(arr1[i], arr2[i])





