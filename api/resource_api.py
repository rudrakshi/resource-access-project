from typing import Union
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

api = FastAPI()

class Resource(BaseModel):
    """
    Resource(id, name, type, is_endangered)
  
    A class to represent a resource.
    
    ...
    
    Attributes
    ----------
    id : int
        identification number of the resource
    name : str
        name of the resource
    type : str
        type of the resource
    is_endangered : bool
        Whether the resorce is abundant or there is a risk of extinction
    """
    id: int
    name: str
    type: str
    is_endangered: bool

resources = dict()

# Mock data used for POC - to be replaced by database in real implementation
resources["1001"] = {
            "id": 1001,
            "name": "dog",
            "type": "Animal",
            "is_endangered": False
        }
resources["1002"] = {
            "id": 1002,
            "name": "palm",
            "type": "Plant",
            "is_endangered": False
        }
resources["1003"] = {
        "id": 1003,
        "name": "gold",
        "type": "Metal",
        "is_endangered": True
    }

@api.get("/resources")
def read_all_resources():
    """Returns all available resources"""
    return resources

@api.get("/resources/{resource_id}", response_model=Resource)
def read_resource(resource_id: str):
    """
    Returns resource information for given 'resource_id'

    Parameters
    ----------
    resource_id : str, mandatory
        identification number of the resource

    Returns
    -------
    Resource object for given 'resource_id'

    Raises
    ------
    HTTPException: 404
        resource for given 'resource_id' is not avaialable
    """
    try:
      return resources[resource_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource does not exist.")

@api.put("/resources/{resource_id}", response_model=Resource)
def update_resource(resource_id: str, resource: Resource):
    """
    Updates resource information for given 'resource_id' with given 'resource' object

    Parameters
    ----------
    resource_id : str, mandatory
        identification number of the resource to be changed

    resource : Resource, mandatory
        resource object with new information

    Returns
    -------
    Resource object with new information

    Raises
    ------
    HTTPException: 404
      resource for given 'resource_id' is not avaialable

    HTTPException: 400
      'resource_id' does not match id in the 'resource' object to be updated
    """
    print(resource.id)
    print(resource_id)
    if str(resource.id) != resource_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Path Resource id does not match with content resource id.")
    if resources.get(resource_id) is not None:
        resources.update({resource_id:resource})
        return resource
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource does not exist.")

@api.post("/resources/{resource_id}", response_model=Resource, status_code=status.HTTP_201_CREATED)
async def create_resource(resource: Resource):
    """
    Creates new resource 

    Parameters
    ----------
    resource : Resource, mandatory
        resource object with new information

    Returns
    -------
    Newly created resource object
    """
    resources[str(resource.id)] = resource
    return resource

@api.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: str):
    """
    Deletes resource information for given 'resource_id'

    Parameters
    ----------
    resource_id : str, mandatory
        identification number of the resource

    Returns
    -------
    None

    Raises
    ------
    HTTPException: 404
        resource for given 'resource_id' is not avaialable
    """
    try:
      resources.pop(resource_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource does not exist.")
    
