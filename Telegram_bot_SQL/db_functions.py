import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="restaurant"
)


def get_all_restaurants():
    global mydb
    mycursor = mydb.cursor()

    sql = 'SELECT * FROM restaurant'
    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result

def insert_restaurant(name: str, address: str):
    global mydb

    mycursor = mydb.cursor()
    sql = "INSERT INTO restaurant (id, name, address) VALUES(NULL, %s, %s)"
    mycursor.execute(sql, (name, address))
    mydb.commit()


def edit_restaurant(id: int, name: str, address: str):
    global mydb

    mycursor = mydb.cursor()
    sql = "UPDATE restaurant Set name = %s, address = %s WHERE id = %s"
    mycursor.execute(sql, (name, address, id))
    mydb.commit()


def delete_restaurant(id: int):
    global mydb

    mycursor = mydb.cursor()
    sql = "DELETE from restaurant WHERE id = " + str(id)
    mycursor.execute(sql)
    mydb.commit()


def get_all_food_types():
    global mydb
    mycursor = mydb.cursor()
    sql = 'SELECT * FROM food_types'
    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result


def insert_food_type(name: str):
    global mydb

    mycursor = mydb.cursor()
    sql = "INSERT INTO food_types (id, name) VALUES(NULL, %s)"
    mycursor.execute(sql, (name, ))
    mydb.commit()


def insert_food(name: str, price: str, description: str, foodtype_id: int, restaurant_id: int):
    global mydb

    mycursor = mydb.cursor()
    sql = "INSERT INTO foods (id, name, price, description, food_type_id, restaurant_id) VALUES(NULL, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, (name, price, description, foodtype_id, restaurant_id))
    mydb.commit()


def get_foods_by_restaurant_id(id):
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description,  ft.name as foodType, r.name as restaurantName " \
        "FROM foods f " \
        "INNER JOIN food_types ft ON ft.id = f.food_type_id " \
        "INNER JOIN restaurant r ON r.id = f.restaurant_id " \
        "WHERE f.restaurant_id = "+str(id)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result


def get_foods_by_food_type(id):
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, ft.name as foodType, r.name as restaurantName " \
          "FROM foods f " \
          "INNER JOIN food_types ft ON ft.id = f.food_type_id " \
          "INNER JOIN restaurant r ON r.id = f.restaurant_id " \
          "WHERE f.food_type_id = " + str(id)
    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result


def get_food(id: int):
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, ft.name as foodType, r.name as restaurantName " \
        "FROM foods f " \
        "INNER JOIN food_types ft ON ft.id = f.food_type_id " \
        "INNER JOIN restaurant r ON r.id = f.restaurant_id " \
        "WHERE f.id = " + str(id)

    mycursor.execute(sql)
    result = mycursor.fetchone()

    return result


def remove_food_type(id: int):
    global mydb
    mycursor = mydb.cursor()

    sql = "DELETE from food_types WHERE id = " + str(id)
    mycursor.execute(sql)
    mydb.commit()

def get_all_foods():
    global mydb
    mycursor = mydb.cursor()

    sql = 'SELECT * FROM foods'
    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result

def remove_food(id: int):
    global mydb
    mycursor = mydb.cursor()

    sql = "DELETE from foods where id = " + str(id)
    mycursor.execute(sql)
    mydb.commit()

def edit_food_type(id: int, name: str):
    global mydb
    mycursor = mydb.cursor()

    sql = "UPDATE food_types Set name = %s WHERE id = %s"
    mycursor.execute(sql, (name, id))
    mydb.commit()

def edit_food(id: int, name: str, price: int, description: str):
    global mydb
    mycursor = mydb.cursor()

    sql = "UPDATE foods Set name = %s, price = %s, description = %s WHERE id = %s"
    mycursor.execute(sql, (name, price, description, id))
    mydb.commit()