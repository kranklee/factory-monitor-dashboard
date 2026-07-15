from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"


class MachineStatus(StrEnum):
    OPERATIONAL = "operational"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


class AlertSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertStatus(StrEnum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
