from enum import Enum

from fastapi import FastAPI, Header, status
from typing import Optional

from pydantic import BaseModel

app = FastAPI()


members: list["Member"] = []
groups: list["Group"] = []


class MemberStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    REJECTED = "rejected"


class Member(BaseModel):
    id: int
    first_name: str
    last_name: str
    address: str
    phone_number: str
    national_id_number: str
    occupation: str
    status: MemberStatus
    group_id: Optional[int] = None


class Group(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    members: list[Member] = []


@app.get("/members", tags=["Members"])
def get_members() -> list[Member]:
    return members


@app.post("/members", status_code=status.HTTP_201_CREATED, tags=["Members"])
def create_member(member: Member) -> dict:
    members.append(member)
    return {"message": "Member created successfully", "member_id": member.id}


@app.get("/members/{member_id}", tags=["Members"])
def get_member(member_id: int) -> Member | dict:
    for member in members:
        if member.id == member_id:
            return member
    return {"message": "Member not found"}


@app.put("/members/{member_id}", tags=["Members"])
def update_member(member_id: int, updated_member: Member) -> dict:
    for index, member in enumerate(members):
        if member.id == member_id:
            members[index] = updated_member
            return {"message": "Member updated successfully", "member": updated_member}
    return {"message": "Member not found"}


@app.delete(
    "/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Members"]
)
def delete_member(member_id: int) -> None:
    for index, member in enumerate(members):
        if member.id == member_id:
            del members[index]
            return
    return {"message": "Member not found"}


@app.get("/groups", tags=["Groups"])
def get_groups() -> list[Group]:
    return groups


@app.post("/groups", status_code=status.HTTP_201_CREATED, tags=["Groups"])
def create_group(group: Group) -> dict:
    groups.append(group)
    return {"message": "Group created successfully", "group_id": group.id}


@app.get("/groups/{group_id}", tags=["Groups"])
def get_group(group_id: int) -> Group | dict:
    for group in groups:
        if group.id == group_id:
            return group
    return {"message": "Group not found"}


@app.put("/groups/{group_id}", tags=["Groups"])
def update_group(group_id: int, updated_group: Group) -> dict:
    for index, group in enumerate(groups):
        if group.id == group_id:
            groups[index] = updated_group
            return {"message": "Group updated successfully", "group": updated_group}
    return {"message": "Group not found"}


@app.delete(
    "/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Groups"]
)
def delete_group(group_id: int) -> None:
    for index, group in enumerate(groups):
        if group.id == group_id:
            del groups[index]
            return
    return {"message": "Group not found"}


@app.post(
    "/groups/{group_id}/members/{member_id}",
    status_code=status.HTTP_200_OK,
    tags=["Groups"],
)
def add_member_to_group(group_id: int, member_id: int) -> dict:
    group = next((g for g in groups if g.id == group_id), None)
    member = next((m for m in members if m.id == member_id), None)

    if not group:
        return {"message": "Group not found"}
    if not member:
        return {"message": "Member not found"}

    if member in group.members:
        return {"message": "Member already in group"}

    group.members.append(member)
    return {"message": "Member added to group successfully"}


@app.delete(
    "/groups/{group_id}/members/{member_id}",
    status_code=status.HTTP_200_OK,
    tags=["Groups"],
)
def remove_member_from_group(group_id: int, member_id: int) -> dict:
    group = next((g for g in groups if g.id == group_id), None)
    member = next((m for m in members if m.id == member_id), None)

    if not group:
        return {"message": "Group not found"}
    if not member:
        return {"message": "Member not found"}

    if member not in group.members:
        return {"message": "Member not in group"}

    group.members.remove(member)
    return {"message": "Member removed from group successfully"}
