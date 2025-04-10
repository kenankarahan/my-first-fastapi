from fastapi import FastAPI
from pydantic import BaseModel, Field
import db_connection as db

app = FastAPI()




# Kullanıcı ve Ürün Modellerini Tanımlama

# Kullanıcı Modeli
class User(BaseModel):
    username : str = Field(min_length=3, max_length=20)
    age : int = Field(ge=18, le=100)
    email : str = Field(pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', default="example@example.com")

# Ürün Modeli
class Product(BaseModel):
    name : str = Field(min_length=3, max_length=50)
    price : float = Field(gt=0)
    category : str = Field(min_length=3, max_length=100)
    quantity : int = Field(gt=0)




# Endpointleri Tanımlama

# İndex
@app.get("/")
async def index():
    return {"message": "Welcome to my first FastAPI application!"}

# Kullanıcı İşlemleri
@app.get("/users")
async def get_users():
    db.cur.execute('SELECT id, username FROM users')
    users = db.cur.fetchall()
    users = [{"id": user[0], "username": user[1]} for user in users]
    return {"users": users}

@app.post("/user/create")
async def create_user(user: User):
    db.cur.execute('INSERT INTO users(username, age, email) VALUES(?, ?, ?)', (user.username, user.age, user.email))
    db.con.commit()
    return {"response" : f"User '{user.username}' created successfully!"}

@app.get("/user/{id}")
async def get_user_details(id: int):
    db.cur.execute('SELECT * FROM users WHERE id=?', (id,))
    user = db.cur.fetchone()
    if user:
        return {"id": user[0], "username": user[1], "age": user[2], "email": user[3], "created_time": user[4]}
    else:
        return {"error": f"User '{user[1]}' not found"}

@app.put("/user/{id}")
async def update_user(id: int, user: User):
    db.cur.execute('UPDATE users SET username=?, age=?, email=? WHERE id=?', (user.username, user.age, user.email, id))
    db.con.commit()
    return {"response" : f"User '{user.username}' updated successfully!"}

@app.delete("/user/delete/{id}")
async def delete_user(id: int):
    db.cur.execute("SELECT username FROM users WHERE id=?", (id,))
    user = db.cur.fetchone()
    username = user[0]
    db.cur.execute('DELETE FROM users WHERE id=?', (id,))
    db.con.commit()
    return {"response" : f"User '{username}' deleted successfully!"}

# Ürün İşlemleri
@app.get("/products")
async def get_products():
    db.cur.execute('SELECT id, name, category FROM products')
    products = db.cur.fetchall()
    products = [{"id": product[0], "name": product[1], "category": product[2]} for product in products]
    return {"products": products}

@app.post("/product/create")
async def create_product(product: Product):
    db.cur.execute('INSERT INTO products(name, price, category, quantity) VALUES(?, ?, ?, ?)', (product.name, product.price, product.category, product.quantity))
    db.con.commit()
    return {"response" : f"Product '{product.name}' created successfully!"}

@app.get("/product/{id}")
async def get_product_details(id: int):
    db.cur.execute('SELECT * FROM products WHERE id=?', (id,))
    product = db.cur.fetchone()
    if product:
        return {"id": product[0], "name": product[1], "price": product[2], "category": product[3], "quantity": product[4], "created_time": product[5]}
    else:
        return {"error": f"Product '{product[1]}' not found"}

@app.put("/product/{id}")
async def update_product(id: int, product: Product):
    db.cur.execute('UPDATE products SET name=?, price=?, category=?, quantity=? WHERE id=?', (product.name, product.price, product.category, product.quantity, id))
    db.con.commit()
    return {"response" : f"Product '{product.name}' updated successfully!"}

@app.delete("/product/delete/{id}")
async def delete_product(id: int):
    db.cur.execute("SELECT name FROM products WHERE id=?", (id,))
    product = db.cur.fetchone()
    name = product[0]
    db.cur.execute('DELETE FROM products WHERE id=?', (id,))
    db.con.commit()
    return {"response" : f"Product '{name}' deleted successfully!"}
