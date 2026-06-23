from enum import Enum

class MoveType(Enum):
    PROPOSE = "PROPOSE"
    SUPPORT = "SUPPORT"
    CHALLENGE = "CHALLENGE"
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    WITHDRAW = "WITHDRAW"