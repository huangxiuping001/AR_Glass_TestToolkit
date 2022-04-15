import pymysql


class Database():
    '''
        Description:
            database demo to store image in MySQL RDBMS
        Attributes:
            None
    '''


def __init__(self):
    self.connection = pymysql.connect(host='localhost', user='root', passwd='monica001.', db='arglass',
                                      charset='utf8')
    self.cursor = self.connection.cursor()

    '''
        Description:
            create table to store images
        Args:
            None
        Return:
            None
    '''


def create_image_table(self):
    sql = """create table if not exists picture (\
            id int, image longblob);"""

    try:
        self.cursor.execute(sql)

        self.connection.commit()

    except pymysql.Error:
        print(pymysql.Error)

    '''
        Description:
            insert image into table
        Args:
            image:
                image to store
        Returns:
            None
    '''


def insert_image(self, image):
    sql = "insert into picture(image) values(%s)"
    self.cursor.execute(sql, image)
    self.connection.commit()

    '''
        Description:
            get image from database
        Args:
            path:
                path to save image
        Returns:
            None
    '''


def get_image(self, path):
    sql = 'select * from picture'
    try:
        self.cursor.execute(sql)
        image = self.cursor.fetchone()[0]
        with open(path, "wb") as file:
            file.write(image)
    except pymysql.Error:
        print(pymysql.Error)
    except IOError:
        print(IOError)

    '''
        Description:
            destruction method
        Args:
            None
        Returns:
            None
    '''


def __del__(self):
    self.connection.close()
    self.cursor.close()


if __name__ == "__main__":
    database = Database()
    # read image from current directory
    with open("./ArithmeticOCR2.jpg", "rb") as file:
        image = file.read()

    database.create_image_table()
    database.insert_image(image)

    database.get_image('./result.jpg')
