from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    phone: str
    email: EmailStr
    address: str
    postalZip: str
    region: str
    country: str
