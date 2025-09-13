from pydantic import BaseModel
from enum import Enum


class CountryCode(str, Enum):
    IN = "IN"  # India
    US = "US"  # United States
    GB = "GB"  # United Kingdom
    CA = "CA"  # Canada
    AU = "AU"  # Australia
    DE = "DE"  # Germany
    FR = "FR"  # France
    SG = "SG"  # Singapore
    JP = "JP"  # Japan
    CN = "CN"  # China


class Timezone(str, Enum):
    IST = "Asia/Kolkata"
    UTC = "UTC"
    PST = "America/Los_Angeles"
    EST = "America/New_York"
    CET = "Europe/Berlin"
    # 👉 add more as needed


class FraudCheckRequest(BaseModel):
    user_id: str
    ip_country: CountryCode
    ip_timezone: Timezone
    device_hash: str
    login_at: str  # ISO 8601 format


class FraudCheckResponse(BaseModel):
    success: bool
