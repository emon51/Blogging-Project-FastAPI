from database import collection 

posts = collection.find()  

print("All posts (MongoDB):\n")
for post in posts:
    print(f"Post-type: {type(post)}")
    print(f"Id-type: {type(post['_id'])}")
    print(f"ID: {post['_id']}")
    print(f"Title: {post['title']}")
    print(f"Content: {post['content']}")
    print("-" * 75)
