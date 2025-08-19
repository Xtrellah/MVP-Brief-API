from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
import databases

# Set up database connection (adjust with actual credentials)
DATABASE_URL = "mysql+asyncmy://user:password@localhost/db_name"
database = databases.Database(DATABASE_URL)

router = APIRouter(
    prefix="/challenges",
    tags=["challenges"]
)


@router.get("/", response_class=JSONResponse)
async def get_challenge_data():
    query = "SELECT * FROM challenges"
    results = await database.fetch_all(query=query)

    if not results:
        raise HTTPException(status_code=404, detail="No challenge data found.")

    data = []

    for challenge in results:
        item = {
            "id": challenge["id"],
            "params": {
                "skill": challenge["skill"],
                "industry": challenge["industry"],
                "experience": challenge["experience"],
            },
            "brief": {
                "scenario": challenge["scenario"],
                "challenge": challenge["challenge"],
                "task": challenge["task"],
            }
        }
        data.append(item)

    return data


@router.get("/filter", response_class=JSONResponse)
async def get_challenge(
    skill: str = Query(default=None),
    industry: str = Query(default=None),
    experience: str = Query(default=None)
):
    query = "SELECT * FROM challenges WHERE TRUE"
    values = {}

    if skill:
        query += " AND JSON_CONTAINS(skill, :skill)"
        values["skill"] = f'"{skill}"'

    if industry:
        query += " AND LOWER(industry) = LOWER(:industry)"
        values["industry"] = industry

    if experience:
        query += " AND LOWER(experience) = LOWER(:experience)"
        values["experience"] = experience

    query += " LIMIT 1"

    result = await database.fetch_one(query=query, values=values)

    if not result:
        return await get_random_challenge()

    item = {
        "brief": {
            "scenario": result["scenario"],
            "challenge": result["challenge"],
            "task": result["task"],
        }
    }

    return item


@router.get("/random", response_class=JSONResponse)
async def get_random_challenge():
    query = """
        SELECT scenario, challenge, task
        FROM challenges
        ORDER BY RAND()
        LIMIT 1
    """
    result = await database.fetch_one(query)

    if not result:
        raise HTTPException(status_code=404, detail="No challenge data found.")

    return {"brief": dict(result)}
