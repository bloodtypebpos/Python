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
        self.code_stats_total = []
        self.code_stats_complete = []
        self.customer = 'Ergotronix'
        for code in self.codes:
            rows, complete_rows = self.get_codes(self.items, code[0])
            self.code_items.append(rows)
            self.code_stats_total.append(len(rows))
            self.completed_code_items.append(complete_rows)
            self.code_stats_complete.append(len(complete_rows))
        if self.sonum == "NA":
            pass
        else:
            query = 'SELECT DISTINCT Customer FROM "' + table + '" WHERE "Reference No" IS "' + sonum + '"'
            rows = self.get_rows(query)
            self.customer = rows[0][0]
        self.image_url = "NA"
        if self.sonum == "NA":
            pass
        else:
            query = 'SELECT Attachments FROM "' + table + '" WHERE "Reference No" = "' + sonum + '" AND "Code" = "Image"'
            rows = self.get_rows(query)
            self.image_url = rows[0][0]
        self.moi = []
        self.moi_codes = ['Machine', 'Order', 'Inventory']
        for code in self.moi_codes:
            for i in range(0, len(self.codes)):
                if code == self.codes[i][0]:
                    self.moi.append(i)
                    break
        self.code_stats_total.append(sum(self.code_stats_total[i] for i in self.moi))
        self.code_stats_complete.append(sum(self.code_stats_complete[i] for i in self.moi))
        self.subassemblies_names = ["NA"]
        if self.sonum == 'NA':
            pass
        else:
            query = query = 'SELECT DISTINCT "Sub Assembly" FROM "' + table + '" WHERE "Reference No" = "' + sonum + '"'
            rows = self.get_rows(query)
            self.subassemblies_names = []
            for row in rows:
                self.subassemblies_names.append(row[0])
        if sonum == "NA":
            pass
        else:
            self.subassemblies = self.get_subassemblies(self.items, self.subassemblies_names)





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

    def get_subassemblies(self, items, subassemblies_names):
        subassemblies = []
        for subassembly in subassemblies_names:
            rows = []
            for item in items:
                if getattr(item, 'Sub Assembly') == subassembly:
                    rows.append(item)
            subassemblies.append(rows)
        return subassemblies



class Item:
    def __init__(self):
        self.test = 'Hello World'

    def update_property(self, property, value):
       setattr(self, property, value)

    def make_attrs(self, arr1, arr2):
        for i in range(0, len(arr1)):
            self.update_property(arr1[i], arr2[i])



class Project3:
    def __init__(self, conn, query):
        self.conn = conn
        self.c = conn.cursor()
        rows = [row for row in self.c.execute(query)]
        self.fields = [field[0] for field in self.c.description]
        self.items = []
        for row in rows:
            item = Item()
            item.make_attrs(self.fields, row)
            self.items.append(item)


class Project4:
    def __init__(self, columns, rows):
        self.fields = columns
        self.items = []
        for row in rows:
            item = Item()
            item.make_attrs(self.fields, row)
            self.items.append(item)


class Airtable_DB:
    def __init__(self, base_key, api_key, conn, c, tab_name, view_name, table_name, ints, floats, ignores):
        self.base_key = base_key
        self.api_key = api_key
        self.conn = conn
        self.c = c
        self.tab_name = tab_name
        self.view_name = view_name
        self.table_name = table_name
        self.ints = ints
        self.floats = floats
        self.ignores = ignores

        airtable = Airtable(self.base_key, self.tab_name, self.api_key)
        records = airtable.get_all(view=self.view_name)
        fields = set()
        for record in records:
            for field in list(record['fields'].keys()):
                fields.add(field)
        fields = list(fields)
        ints = self.ints
        floats = self.floats
        ignores = self.ignores

        recs = []
        for record in records:
            rec = []
            for field in fields:
                try:
                    if field in ints:
                        rec.append(int(record['fields'][field]))
                    elif field in floats:
                        rec.append(float(record['fields'][field]))
                    elif field in ignores:
                        if field == 'Attachments':
                            rec.append(record['fields'][field][0]['url'])
                        else:
                            pass
                    else:
                        rec.append(record['fields'][field])
                except:
                    if field in ints:
                        rec.append(0)
                    elif field in floats:
                        rec.append(0.0)
                    elif field in ignores:
                        if field == 'Attachments':
                            rec.append('NA')
                        else:
                            pass
                    else:
                        rec.append("NA")
            recs.append(rec)

        table_name = self.table_name
        self.make_air_table(fields, table_name, ints, floats, ignores)
        self.fill_air_table(fields, table_name, recs, ints, floats, ignores)

    def make_air_table(self, fields, table_name, ints, floats, ignores):
        for i in range(0, len(fields)):
            if '"' in fields[i]:
                fields[i].replace('"', '``')
            if "'" in fields[i]:
                fields[i].replace("'", '`')
        self.c.execute('DROP TABLE IF EXISTS "' + table_name + '"')
        query = 'CREATE TABLE "' + table_name + '"(id INTEGER PRIMARY KEY,'
        for field in fields:
            if field in ints:
                query = query + ' "' + field + '" INTEGER,'
            elif field in floats:
                query = query + ' "' + field + '" REAL,'
            elif field in ignores:
                if field == 'Attachments':
                    query = query + ' "' + field + '" TEXT,'
                else:
                    pass
            else:
                query = query + ' "' + field + '" TEXT,'
        query = query[:-1] + ')'
        self.c.execute(query)
        self.conn.commit()

    def fill_air_table(self, fields, table_name, recs, ints, floats, ignores):
        for record in recs:
            query = 'INSERT INTO "' + table_name + '"('
            for def_i in range(0, len(fields)):
                field = fields[def_i]
                if field in ignores:
                    if field == 'Attachments':
                        query = query + ' "' + field + '",'
                    else:
                        pass
                else:
                    query = query + ' "' + field + '",'
            query = query[:-1] + ') VALUES ('
            for def_i in range(0, len(fields)):
                field = fields[def_i]
                if field in ignores:
                    if field == 'Attachments':
                        query = query + '?,'
                    else:
                        pass
                else:
                    query = query + '?,'
            query = query[:-1] + ')'
            self.c.execute(query, record)
        self.conn.commit()
