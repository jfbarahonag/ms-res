from enum import Enum

class ReversalType(str, Enum):
    porErroresOperativos = "Reversion por errores operativos"
    porErroresCliente = "Reversion por errores del cliente"