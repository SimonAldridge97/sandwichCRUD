from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .controllers import order_details

from .models import models, schemas
from .controllers import orders, sandwiches, resources, recipes
from .dependencies.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)


@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)


@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return order


@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order_db = orders.read_one(db, order_id=order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.update(db=db, order=order, order_id=order_id)


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.delete(db=db, order_id=order_id)

#### Sandwich portion #####
@app.post("/sandwich/", response_model=schemas.Sandwich, tags=["Sandwiches"])
def create_sandwich(sandwich: schemas.SandwichCreate, db: Session = Depends(get_db)):
    return sandwiches.create(sandwich=sandwich, db=db)

@app.get("/sandwich/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def read_one_sandwich(sandwich_id: int, db: Session= Depends(get_db)):
    sandwich = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if sandwich is None:
        raise HTTPException(status_code=404, detail=f"Sandwich with id {sandwich_id} does not exist.")
    return sandwich

@app.get("/sandwich/", response_model=list[schemas.Sandwich], tags=["Sandwiches"])
def read_all_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)

@app.put("/sanwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def update_one_sandwich(sandwich_id: int, sandwich: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    db_sandwich = sandwiches.read_one(db, sandwich_id = sandwich_id)
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail=f"Sandwich with id {sandwich_id} not found.")
    return sandwiches.update(db=db, sandwich=sandwich, sandwich_id=sandwich_id)

@app.delete("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def delete_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if sandwich is None:
        raise HTTPException(status_code=404, detail=f"Sandwich with id {sandwich_id} not found.")
    return sandwiches.delete(db=db, sandwich_id = sandwich_id)

#### End Sandwich portion ####

### Resource portion ###

@app.post("/resource/", response_model=schemas.Resource, tags=["Resources"])
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return resources.create(resource=resource, db=db)

@app.get("/resource/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def read_one_resource(resource_id: int, db : Session = Depends(get_db)):
    resource = resources.read_one(db, resource_id=resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail=f"Resource with id {resource_id} not found.")
    return resource

@app.get("/resources/", response_model=list[schemas.Resource], tags=["Resources"])
def read_all_resources(db: Session = Depends(get_db)):
    return resources.read_all(db)

@app.put("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def update_one_resource(resource_id: int, resource: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    db_resource = resources.read_one(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail=f"Resource with id {resource_id} not found.")
    return resources.update(db=db, resource=resource, resource_id=resource_id)

@app.delete("/resources/{resource_id}", tags=["Resources"])
def delete_one_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = resources.read_one(db, resource_id=resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail=f"Resource with id {resource_id} not found.")
    return resources.delete(db=db, resource_id=resource_id)

### End Resource Portion ### 

### Recipes Section ###
@app.post("/recipe/", response_model=schemas.Recipe, tags=["Recipes"])
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return recipes.create(recipe=recipe, db=db)

@app.get("/recipe/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def read_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = recipe.read_one(db, recipe_id = recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail=f"Resource with id {recipe_id} not found.")
    return recipe

@app.get("/recipes/", response_model=list[schemas.Recipe], tags=['Recipes'])
def read_all_recipe(db: Session = Depends(get_db)):
    return recipes.read_all(db)

@app.put("/recipe/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def update_one_recipe(recipe_id: int, recipe: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    db_recipe = recipes.read_one(db=db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail=f"Resource with id {recipe_id} not found.")
    return recipes.update(db=db, recipe=recipe, recipe_id=recipe_id)

@app.delete("/recipe/{recipe_id}", tags=["Recipes"])
def delete_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = recipes.read_one(db, resource_id=recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail=f"Resource with id {recipe_id} not found.")
    return recipes.delete(db=db, resource_id=recipe_id)
###End Recipes Section###

### Order_Details Section ###
@app.post("/order_detail/", response_model=schemas.OrderDetail, tags=["Order_Details"])
def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    return order_detail.create(order_detail=order_detail, db=db)

@app.get("/order_detail/{order_detail_id}", response_model=schemas.OrderDetail, tags=["Order_Details"])
def read_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = order_details.read_one(db, order_detail_id = order_detail_id)
    if order_detail is None:
        raise HTTPException(status_code=404, detail=f"Resource with id {order_detail_id} not found.")
    return order_detail

@app.get("/order_detail/", response_model=list[schemas.OrderDetail], tags=['Order_Details'])
def read_all_order_detail(db: Session = Depends(get_db)):
    return order_details.read_all(db)

@app.put("/order_detail/{order_detail_id}", response_model=schemas.OrderDetail, tags=["Order_Details"])
def update_one_order_detail(order_detail_id: int, recipe: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    db_order_detail = order_details.read_one(db=db, order_detail_id = order_detail_id)
    if db_order_detail is None:
        raise HTTPException(status_code=404, detail=f"Resource with id {order_detail_id} not found.")
    return order_details.update(db=db, order_details=order_details, order_detail_id=order_detail_id)

@app.delete("/order_detail/{order_detail_id}", tags=["Order_Details"])
def delete_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = order_details.read_one(db, order_detail_id=order_detail_id)
    if order_detail is None:
        raise HTTPException(status_code=404, detail=f"Resource with id {order_detail_id} not found.")
    return order_details.delete(db=db, order_detail_id=order_detail_id)






### End Order_details Section ###