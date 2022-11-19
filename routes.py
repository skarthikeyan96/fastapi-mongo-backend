from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List


from models import ListModel, ListUpdateModel

router = APIRouter()


@router.post("/", response_description='create a todo list', status_code=status.HTTP_201_CREATED,response_model=ListModel)
def create_list(request: Request, list: ListModel = Body(...)):
    list = jsonable_encoder(list)
    new_list = request.app.database["lists"].insert_one(list)
    created_list = request.app.database["lists"].find_one({
        "_id": new_list.inserted_id
    })

    return created_list


@router.get("/", response_description="list all the todos", response_model=List[ListModel])
def show_list(request: Request):
    todos = list(request.app.database["lists"].find(limit=50))
    return todos

@router.delete("/",response_description="delete a item from list")
def delete_list(id: str, request: Request, response: Response):
    delete_result = request.app.database["lists"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Book with {id} not found")


# # getting one element from the list

@router.put("/",response_description="update the item in list", response_model=ListModel)
def update_item(id: str, request: Request, list: ListUpdateModel = Body(...)):
    # print("update list route", list.dict())  # {'title': 'string', 'description': 'string'}
    # update a single document
    update_result = request.app.database["lists"].update_one({"_id": id }, {"$set": {"title": list.title, "description" : list.description} })
    # print("update result ",update_result.modified_count)

    if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Item with ID {id} has not been modified")
    

    if (
        updated_list_item := request.app.database["lists"].find_one({"_id": id})
    ) is not None:
        return updated_list_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ListItem with ID {id} not found")
    
