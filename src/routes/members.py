
from fastapi import APIRouter, Header, status
from src.schemas.members import Member

member_router = APIRouter(prefix='/members', tags=["members"])


members: list["Member"] = []

@member_router.get("/")
def get_members() -> list[Member]:
    return members


@member_router.post("/", status_code=status.HTTP_201_CREATED)
def create_member(member: Member) -> dict:
    members.append(member)
    return {"message": "Member created successfully", "member_id": member.id}


@member_router.get("/{member_id}")
def get_member(member_id: int) -> Member | dict:
    for member in members:
        if member.id == member_id:
            return member
    return {"message": "Member not found"}


@member_router.put("/{member_id}")
def update_member(member_id: int, updated_member: Member) -> dict:
    for index, member in enumerate(members):
        if member.id == member_id:
            members[index] = updated_member
            return {"message": "Member updated successfully", "member": updated_member}
    return {"message": "Member not found"}


@member_router.delete(
    "/{member_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_member(member_id: int) -> None:
    for index, member in enumerate(members):
        if member.id == member_id:
            del members[index]
            return
    return {"message": "Member not found"}