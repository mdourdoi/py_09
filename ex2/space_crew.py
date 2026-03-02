from enum import Enum
from pydantic import BaseModel, model_validator, Field, ValidationError
from datetime import datetime


class Rank(str, Enum):
    cadet = 'cadet'
    officer = 'officer'
    lieutenant = 'lieutenant'
    captain = 'captain'
    commander = 'commander'


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default='planned')
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def mission_validation(self) -> 'SpaceMission':
        if not self.mission_id.startswith('M'):
            raise ValueError('Mission ID must start with "M"')
        in_charge_found = False
        exp = 0
        for crewmate in self.crew:
            if not crewmate.is_active:
                raise ValueError('All crew members must be active')
            if crewmate.rank in [Rank.captain, Rank.commander]:
                in_charge_found = True
            if crewmate.years_experience >= 5:
                exp += 1
        if not in_charge_found:
            raise ValueError('Must have at least one Commander or Captain')
        if self.duration_days > 365 and not exp / len(self.crew) >= 0.5:
            raise ValueError("Long missions need 50% experienced crew")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2024-06-01T09:00:00",
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                {
                    "member_id": "CM001",
                    "name": "Sarah Connor",
                    "rank": "commander",
                    "age": 42,
                    "specialization": "Mission Command",
                    "years_experience": 12,
                    "is_active": True,
                },
                {
                    "member_id": "CM002",
                    "name": "John Smith",
                    "rank": "lieutenant",
                    "age": 33,
                    "specialization": "Navigation",
                    "years_experience": 6,
                    "is_active": True,
                },
                {
                    "member_id": "CM003",
                    "name": "Alice Johnson",
                    "rank": "officer",
                    "age": 29,
                    "specialization": "Engineering",
                    "years_experience": 2,
                    "is_active": True,
                },
            ],
        )

        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(f"- {member.name} ({member.rank.value}) - "
                  f"{member.specialization}")
        print()
        print("=========================================")
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="No Leader Mission",
            destination="Moon",
            launch_date="2024-06-01T09:00:00",
            duration_days=900,
            budget_millions=100.0,
            crew=[
                {
                    "member_id": "CM010",
                    "name": "Bob Example",
                    "rank": "lieutenant",
                    "age": 35,
                    "specialization": "Navigation",
                    "years_experience": 10,
                    "is_active": True,
                }
            ],
        )

    except ValidationError as cur_error:
        print("Expected validation error:")
        print(cur_error.errors()[0]['ctx']['error'])


if __name__ == "__main__":
    try:
        main()
    except Exception as cur_error:
        print('Error:', cur_error)
