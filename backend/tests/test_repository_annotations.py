from typing import get_type_hints

from app.models.alert import Alert
from app.models.enums import MachineStatus
from app.repositories.alerts import AlertRepository
from app.repositories.machines import MachineRepository


def test_repository_list_method_does_not_shadow_builtin_list_annotations() -> None:
    alert_hints = get_type_hints(AlertRepository.recent)
    machine_hints = get_type_hints(MachineRepository.summary)

    assert alert_hints["return"] == list[Alert]
    assert machine_hints["return"] == tuple[int, int, float, float, list[tuple[MachineStatus, int]]]
