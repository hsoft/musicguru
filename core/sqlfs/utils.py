# Created By: Virgil Dupras
# Created On: 2006/10/07
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

def escape(s, to_escape, escape_with='\\'):
    return ''.join((escape_with+c if c in to_escape else c) for c in s)

def sqlite_escape(s):
    return escape(s, "'", "'")

class DBBuffer:
    """Progressively buffers a SQL SELECT request, using LIMIT
    """
    def __init__(self,con,sql,lookahead=10):
        self.con = con
        self.sql = sql
        self.lookahead = lookahead
        self.count = None
        self.buffer = []
    
    def __len__(self):
        if self.count is None:
            cur = self.con.execute("select count(*) from (%s)" % self.sql)
            self.count = cur.fetchone()[0]
        return self.count
    
    def __getitem__(self,key):
        if key < 0:
            raise IndexError("DBBuffer is of an unknown length. Negative indexes not supported.")
        if key >= len(self.buffer):
            start = len(self.buffer)
            end = key + self.lookahead + 1
            cur = self.con.execute("%s limit %d,%d" % (self.sql,start,end))
            for row in cur:
                if len(row) == 1:
                    row = row[0]
                self.buffer.append(row)
        return self.buffer[key]
    
    def fetchall(self):
        cur = self.con.execute(self.sql)
        result = []
        for row in cur:
            if len(row) == 1:
                row = row[0]
            result.append(row)
        return result
    

def attr_values_of_nodes(con,attr_name,node_ids=None):
    """Get a list of all values for attr 'attr_name' for nodes 'nodes'.
    
    con: a SQLite connection
    attr_name: The name of the attr values to fetch.
    node_ids: a list of ids to fetch values from.
    Returns a list of values (can be string or int).
    """
    if node_ids is None:
        where = "where name = '%s' and value <> ''" % attr_name
    else:
        ids = (str(id) for id in node_ids)
        where = "where name = '%s' and parent in (%s) and value <> ''" % (attr_name, ','.join(ids))
    sql = "select distinct value from attrs %s order by lower(value)" % where
    return DBBuffer(con,sql)

def attr_sum_of_nodes(con,attr_name,node_ids=None):
    """Get the SUM() of node_ids's values for attr_name.
    
    con: a SQLite connection
    attr_name: The name of the attr values to fetch.
    node_ids: a list of ids to sompute the sum from.
    Returns a number that is the requested sum.
    """
    if node_ids is None:
        sql = "select sum(value) from attrs where name = '%s' group by name" % attr_name
    else:
        ids = (str(id) for id in node_ids)
        sql = "select sum(value) from attrs where name = '%s' and parent in (%s) group by name" % (attr_name, ','.join(ids))
    cur = con.execute(sql)
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return 0

def nodes_of_attr_values(con,attr_name,attr_values):
    """Get a list of node ids that have a attr 'attr_name' with a value in 'attr_values'.
    
    con: a SQLite connection
    attr_name: The name of the attr values to fetch.
    attr_values: a list of values you want your nodes to match with.
    returns a list of *ids*. use nodes_of_ids() to get node objects.
    """
    if not attr_values:
        return []
    attr_values = (sqlite_escape(value) for value in attr_values)
    sql = "select parent from attrs where name = '%s' and value in ('%s')" % (attr_name, '\',\''.join(attr_values))
    return DBBuffer(con,sql)
