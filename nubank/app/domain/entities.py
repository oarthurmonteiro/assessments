from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

class TransferStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REVERSED = "REVERSED"

@dataclass
class Transfer:
    source_id: str
    destiny_id: str
    amount: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TransferStatus = TransferStatus.PENDING
    timestamp: datetime = field(default_factory=datetime.now)