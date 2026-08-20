import sqlite3

from fastapi import FastAPI, HTTPException, status
from database import (
    create_customer,
    delete_customer,
    get_customer_by_id,
    init_db,
    list_all_customers,
    update_customer,
)
from schemas import Customer, CustomerCreate, CustomerUpdate

init_db()

app = FastAPI()


@app.get("/customers", status_code=status.HTTP_200_OK)
async def get_all_customers() -> list[Customer]:
    customers = list_all_customers()
    return [Customer(**x) for x in customers]


@app.post("/customers", status_code=status.HTTP_201_CREATED)
async def add_customer(create_data: CustomerCreate) -> Customer:
    data_dict = create_data.model_dump()
    try:
        customer_id = create_customer(data_dict)
    except sqlite3.IntegrityError:
        raise HTTPException(
            detail={"message": "A customer with that email, national id or phone number already exists"},
            status_code=status.HTTP_409_CONFLICT,
        )
    return Customer(**get_customer_by_id(customer_id)) # type: ignore


@app.get("/customers/{customer_id}")
async def get_customer(customer_id: int) -> Customer:
    customer = get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(
            detail={"message": "Customer not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return Customer(**customer)


@app.patch("/customers/{customer_id}")
async def update_customer_partial(
    customer_id: int, update_data: CustomerUpdate
) -> Customer:
    customer = get_customer_by_id(customer_id)

    if not customer:
        raise HTTPException(
            detail={"message": "Customer not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    data_dict = update_data.model_dump()
    try:
        updated_customer = update_customer(customer_id, data_dict)

        return Customer(**updated_customer)  # type: ignore
    except sqlite3.DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Failed to update customer"},
        ) from e


@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_customer(customer_id: int) -> None:
    customer = get_customer_by_id(customer_id)

    if not customer:
        raise HTTPException(
            detail={"message": "Customer not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    deleted = delete_customer(customer_id)

    if not deleted:
        raise HTTPException(
            detail={"message": "Failed to delete customer"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
        

