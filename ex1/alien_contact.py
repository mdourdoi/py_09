from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional


class ContactType(str, Enum):
    radio = 'radio'
    visual = 'visual'
    physical = 'physical'
    telepathic = 'telepathic'


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=110)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def check_validation(self) -> 'AlienContact':
        if not self.contact_id.startswith('AC'):
            raise ValueError('Contact ID must start with "AC" (Alien Contact)')
        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError('Physical contact reports must be verified')
        if (self.contact_type == ContactType.telepathic
                and self.witness_count < 3):
            raise ValueError(
                'Telepathic contact requires at least 3 witnesses')
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                'Strong signals (> 7.0) should include received messages')
        return self


def main() -> None:
    try:
        print('Alien Contact Log Validation')
        print('======================================')
        alien_contact = AlienContact(
            contact_id='AC_2024_001',
            timestamp='2024-01-01',
            location='Area 51, Nevada',
            contact_type='radio',
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received='Greetings from Zeta Reticuli'
        )
        print('Valid contact report:')
        print(f'ID: {alien_contact.contact_id}')
        print(f'Type: {alien_contact.contact_type}')
        print(f'Location: {alien_contact.location}')
        print(f'Signal: {alien_contact.signal_strength}/10')
        print(f'Duration: {alien_contact.duration_minutes} minutes')
        print(f'Witnesses: {alien_contact.witness_count}')
        print(f'Message: {alien_contact.message_received}')
        print()
        print('======================================')
        invalid_contact = AlienContact(
            contact_id='AC_2024_002',
            timestamp='2024-01-01',
            location='69 pelo',
            contact_type='telepathic',
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received='Greetings from nothin I am an error'
        )
        print(invalid_contact)
    except (ValidationError, ValueError) as cur_error:
        print('Expected validation error:')
        print(cur_error.errors()[0]['ctx']['error'])


if __name__ == '__main__':
    try:
        main()
    except Exception as cur_error:
        print('Error:', cur_error)
