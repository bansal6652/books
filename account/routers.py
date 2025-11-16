from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["ACCOUNT"])


@router.get("/account")
async def getaccount():
    return {"message" : "Listing the accounts"}

@router.get("/account/{account_name}")
async def get_specific_account(account_name : str):
    return {"message"  : f"Showing account info for user with account name as {account_name}"}


@router.post("/account/addacccount")
async def add_account_of_user():
    return {"message" :  "User has been added"} 

@router.put("/account/addacccount/{accountid}")
async def edit_account_of_user(accountid : int):
    return {"message" :  "User has been modded"} 

@router.delete("/account/deleteccount/{accountid}")
async def remove_account_of_user():
    return {"message" :  "User has been deleted"} 