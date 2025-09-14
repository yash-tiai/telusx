from datetime import datetime

from pydantic import BaseModel
from enum import Enum


class ActivityStatus(str, Enum):
    IN_PROCESS = 'IN_PROCESS'
    COMPLETED = 'COMPLETED'
    PENDING = 'PENDING'


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
    UK = "UK"  # United Kingdom
    RU = "RU"  # Russia


class Timezone(str, Enum):
    IST = "IST"
    PST = "PST"
    EST = "EST"
    CET = "CET"
    GMT = "GMT"
    JST = "JST"
    AEST = "AEST"
    SGT = "SGT"
    CST = "CST"


class IspType(str, Enum):
    residential = "residential"
    datacenter = "datacenter"


class FraudCheckResponse(BaseModel):
    success: bool
    is_anomaly: str
    anomaly_score: float | None


class FraudCheckRequest(BaseModel):
    user_id: str
    ip_country: CountryCode
    ip_timezone: Timezone
    device_hash: str
    login_at: datetime  # ISO 8601 format
    isp_type: IspType  # e.g., "residential", "datacenter"
    vpn_flag: bool  # True if VPN is used, else False


class FraudCheckUser(BaseModel):
    id: int
    user_id: str
    ip_country: str
    ip_timezone: str
    login_at: datetime
    anomaly_score: float | None
    is_anomalous: str | None
    status: ActivityStatus


class FraudUserListResponse(BaseModel):
    data: list[FraudCheckUser] = []
