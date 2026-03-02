from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print('Space Station Data Validation')
    print('========================================')
    try:
        station = SpaceStation(
            station_id='ISS001',
            name='International Space Station',
            crew_size=6,
            power_level=85.5,
            last_maintenance='2024-01-01',
            oxygen_level=92.3)
        print(f'ID: {station.station_id}')
        print(f'Name: {station.name}')
        print(f'Crew: {station.crew_size}')
        print(f'Power: {station.power_level}%')
        print(f'Oxygen: {station.oxygen_level}%')
        print(
            f"Status: {'Operational' if station.is_operational else 'Down'}")
        print()
        print('========================================')
        invalid = station = SpaceStation(
            station_id='ISS002',
            name='International Flop Station',
            crew_size=69,
            power_level=85.5,
            last_maintenance='2024-01-01T10:00:00',
            oxygen_level=92.3)
        print(invalid)
    except ValidationError as cur_error:
        print('Expected validation error:')
        print(cur_error.errors()[0]['msg'])


if __name__ == "__main__":
    try:
        main()
    except Exception as cur_error:
        print('Error:', cur_error)
