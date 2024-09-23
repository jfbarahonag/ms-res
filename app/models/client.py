from enum import Enum

class CompanyDocumentType(str, Enum):
    NIT = "NIT"

class UserDocumentType(str, Enum):
    PASSPORT = "PASAPORTE"
    CC = "CC"