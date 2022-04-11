# -*- coding: utf-8 -*-

import pymysql

class DbTools(object):

    def __init__(self, user, table_name = 'data'):
        self.user = user

        self.table_name = table_name

        self.__openDB()

        self.cursor.execute('show tables')

        tables = self.cursor.fetchall()

        self.db.close()

        if (table_name,) in tables:
            print('table %s already exit'%(table_name))
        else:
            print('create table')
            self.createDataTable()

    def __openDB(self):
        self.db = pymysql.connect(host = '172.31.114.97',
                                  port = 3306,
                                  user = 'root',
                                  passwd = 'Trans!2018',
                                  db = 'data_performance',
                                  charset = 'utf8')
        self.cursor = self.db.cursor()

    def __excuteSqlAndClose(self, sql = '', ifCommit = False):
        try:
            print('excute sql: %s'%(sql))
            self.cursor.execute(sql)

            if ifCommit:
                self.db.commit()
        except Exception as e:
            self.db.rollback()

            print('excute sql Error, sql = %s, msg = %s'%(sql, str(e)))

        self.db.close()

    def createDataTable(self):
        sql = """CREATE TABLE `%s` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `product` char(10) NOT NULL,
                        `rom_version` char(20) NOT NULL,
                        `user` char(20) NOT NULL,
                        `scene` char(20) NOT NULL,
                        `process` varchar(100) NOT NULL,
                        `min` float NOT NULL DEFAULT 0.0,
                        `mid` float NOT NULL DEFAULT 0.0,
                        `max` float NOT NULL DEFAULT 0.0,
                        `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
                        `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        `extra` text,
                        PRIMARY KEY (`id`)
                )AUTO_INCREMENT=0 ENGINE=InnoDB DEFAULT CHARSET=utf8;
                """ % (self.table_name)

        self.executeSQL(sql)

    def createEngineTable(self):
        sql = """CREATE TABLE engine_version (
                                `id` int(11) NOT NULL AUTO_INCREMENT,
                                `product` char(10) NOT NULL,
                                `rom_version` char(20) NOT NULL,
                                `edgeEsr` char(20),
                                `Esr` char(20),
                                `Itrans` char(20),
                                `NiuTrans` char(20),
                                `Letts` char(20),
                                `Imtts` char(20),
                                `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
                                `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                `extra` text,
                                PRIMARY KEY (`id`)
                        )AUTO_INCREMENT=0 ENGINE=InnoDB DEFAULT CHARSET=utf8;
                        """

        self.executeSQL(sql)

    def insertEngine(self, product, rom_version, edgeEsr, Esr, Itrans, NiuTrans, Letts, Imtts, extra = ''):
        sql = """INSERT INTO engine_version(product, rom_version, edgeEsr, Esr, Itrans, NiuTrans, Letts, Imtts, extra) 
                VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s')""" % (
        product, rom_version, edgeEsr, Esr, Itrans, NiuTrans, Letts, Imtts, extra)

        self.executeSQL(sql, True)

    def insert(self, product, rom_version, scene, process, min = 0.0, mid = 0.1, max = 0.0, extra = ''):
        sql = """INSERT INTO %s(product, rom_version, user, scene, process, min, mid, max, extra) 
        VALUES('%s', '%s', '%s', '%s', '%s', %s, %s, %s, '%s')"""%(self.table_name, product, rom_version, self.user, scene, process, min, mid, max, extra)

        self.executeSQL(sql, True)

    def update(self, product, rom_version, scene, process, min = 0.0, mid = 0.0, max = 0.0):

        sql = "UPDATE %s SET min = %s, mid = %s, max = %s WHERE product = '%s' and rom_version = '%s' and scene = '%s' and process = '%s'"%\
        (self.table_name, min, mid, max, product, rom_version, scene, process)

        self.executeSQL(sql, True)

    def query(self, product, rom_version, scene, process):
        self.__openDB()

        sql = "SELECT min, mid, max FROM %s WHERE product = '%s' and rom_version = '%s' and scene = '%s' and process = '%s'"%\
              (self.table_name, product, rom_version, scene, process)

        try:
            self.cursor.execute(sql)

            results = self.cursor.fetchall()

            if len(results) == 0:
                return -1, -1, -1
            else:
                return results[0]
        except Exception as e:
            print('query data error! e= ' + str(e))

            return -1, -1, -1

    def delete(self, product, rom_version, scene):
        self.__openDB()

        sql = "DELETE FROM %s WHERE product = '%s' rom_version = '%s' and scene = '%s'" % (
        self.table_name, product, rom_version, scene)

        self.__excuteSqlAndClose(sql)

    def executeSQL(self, sql, ifCommit = False):
        self.__openDB()

        self.__excuteSqlAndClose(sql, ifCommit)

if __name__ == '__main__':
    dbt = DbTools('zbdai')

    dbt.delete('3.0', '3900', 'voice_trans')