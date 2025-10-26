from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from models import Post
from database import collection
#=============================================================================================

app = FastAPI()
templates = Jinja2Templates(directory="templates")

#=============================================================================================

# Helper function to convert MongoDB object to dict.
def post_serializer(post):
    return {
        "_id": str(post["_id"]),
        "title": post["title"],
        "content": post["content"]
    }
#=============================================================================================

# Home page: list of all posts.
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    posts = [post_serializer(post) for post in collection.find()]
    return templates.TemplateResponse("index.html", context={"request": request, "posts": posts})
#=============================================================================================

# Post creation.

# Step-1: This get request just shows the empty form to the user to create a new post.
@app.get("/create-post", response_class=HTMLResponse)
def create_post(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})

# Step-2: When user submit the form then request type will be 'post' and call this function with filled forms.
@app.post("/create-post")
def create_post(title: str = Form(...), content: str = Form(...)):
    new_post = {"title": title, "content": content}
    collection.insert_one(new_post)
    return RedirectResponse("/", status_code=303)
# Here status_code=303 is used to make fresh get request, so that it can't repeat the previous request ('create-post'). 
# _id field creates automatically in MongoDB database when we insert record to the database.
#=============================================================================================

# Show a single post
@app.get("/post/{post_id}", response_class=HTMLResponse)
def post_detail(request: Request, post_id: str):
    post = collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return HTMLResponse(content="Post not found", status_code=404)
    return templates.TemplateResponse("post_detail.html", {"request": request, "post": post_serializer(post)})

#=============================================================================================

# Update post

# Step-1: Get the form with existing data corresponding post_id.
@app.get("/update-post/{post_id}", response_class=HTMLResponse)
def update_post(request: Request, post_id: str):
    post = collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return HTMLResponse(content="Post not found", status_code=404)
    return templates.TemplateResponse("update_post.html", {"request": request, "post": post_serializer(post)})

# Step-2: When user submit the edited-form then request type will be 'post' and call this function with newly filled forms.
@app.post("/update-post/{post_id}")
def update_post(post_id: str, title: str = Form(...), content: str = Form(...)):
    updated_post = {"title": title, "content": content}
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": updated_post}
    )
    return RedirectResponse("/", status_code=303)

# Syntax: collection.find_one(filter, projection=None)
# Syntax: collection.update_one(filter, update)

# filter-parameter takes a dictionary specifying the condition for selecting a record.
# projection-parameter is optional takes a dictionary specifying which fields to include(1) or exclude(0) by setting value 1 and 0 of the keys/attributes.
# update-parameter takes a dictionary data to update.
# $set is a MongoDB update operator.

#=============================================================================================



# Delete post 
@app.get("/delete-post/{post_id}")
def delete_post(post_id: str):
    collection.delete_one({"_id": ObjectId(post_id)})
    return RedirectResponse("/", status_code=303)

# Syntax: collection.delete_one(filter)
# filter-parameter takes a dictionary specifying which document to delete


#=============================================================================================













