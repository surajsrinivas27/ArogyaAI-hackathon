from fastapi import APIRouter, Depends
import app.database as db

from app.models.family import FamilyMemberCreate
from app.utils.security import get_current_user

router = APIRouter(
    prefix="/family",
    tags=["Family"]
)


@router.post("/add")
async def add_family_member(
    member: FamilyMemberCreate,
    current_user: str = Depends(get_current_user)
):
    member_data = member.model_dump()

    member_data["owner_email"] = current_user

    await db.database.family.insert_one(member_data)

    return {
        "message": "Family member added successfully"
    }


@router.get("/all")
async def get_family_members(
    current_user: str = Depends(get_current_user)
):
    members = await db.database.family.find(
        {
            "owner_email": current_user
        },
        {
            "_id": 0
        }
    ).to_list(100)

    return members