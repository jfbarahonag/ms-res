from enum import Enum

class MaintenanceInfoType(str, Enum):
    DATETIME = "datetime",
    DATE = "date",
    TEXT = "text"

class MaintenanceType(int, Enum):
    REVERSAL = 1
    TYPE_2 = 2
    TYPE_3 = 3
    TYPE_4 = 4
    TYPE_5 = 5
    TYPE_OTHER = 6