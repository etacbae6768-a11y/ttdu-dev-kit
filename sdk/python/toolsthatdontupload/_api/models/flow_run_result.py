from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_run_result_notes_item import FlowRunResultNotesItem
    from ..models.output_file import OutputFile
    from ..models.step_state import StepState


T = TypeVar("T", bound="FlowRunResult")


@_attrs_define
class FlowRunResult:
    """
    Attributes:
        ok (bool):
        outputs (list[OutputFile]):
        steps (list[StepState] | Unset):
        notes (list[FlowRunResultNotesItem] | Unset): Remarks from steps, e.g. a masking step that found nothing in a
            file
    """

    ok: bool
    outputs: list[OutputFile]
    steps: list[StepState] | Unset = UNSET
    notes: list[FlowRunResultNotesItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        outputs = []
        for outputs_item_data in self.outputs:
            outputs_item = outputs_item_data.to_dict()
            outputs.append(outputs_item)

        steps: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item = steps_item_data.to_dict()
                steps.append(steps_item)

        notes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.notes, Unset):
            notes = []
            for notes_item_data in self.notes:
                notes_item = notes_item_data.to_dict()
                notes.append(notes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ok": ok,
                "outputs": outputs,
            }
        )
        if steps is not UNSET:
            field_dict["steps"] = steps
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.flow_run_result_notes_item import FlowRunResultNotesItem
        from ..models.output_file import OutputFile
        from ..models.step_state import StepState

        d = dict(src_dict)
        ok = d.pop("ok")

        outputs = []
        _outputs = d.pop("outputs")
        for outputs_item_data in _outputs:
            outputs_item = OutputFile.from_dict(outputs_item_data)

            outputs.append(outputs_item)

        _steps = d.pop("steps", UNSET)
        steps: list[StepState] | Unset = UNSET
        if _steps is not UNSET:
            steps = []
            for steps_item_data in _steps:
                steps_item = StepState.from_dict(steps_item_data)

                steps.append(steps_item)

        _notes = d.pop("notes", UNSET)
        notes: list[FlowRunResultNotesItem] | Unset = UNSET
        if _notes is not UNSET:
            notes = []
            for notes_item_data in _notes:
                notes_item = FlowRunResultNotesItem.from_dict(notes_item_data)

                notes.append(notes_item)

        flow_run_result = cls(
            ok=ok,
            outputs=outputs,
            steps=steps,
            notes=notes,
        )

        flow_run_result.additional_properties = d
        return flow_run_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
