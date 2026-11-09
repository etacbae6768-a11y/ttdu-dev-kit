from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_schema import FlowSchema
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_step import FlowStep
    from ..models.flow_var import FlowVar


T = TypeVar("T", bound="Flow")


@_attrs_define
class Flow:
    """A saved flow (ttdu.flow/v1).

    Attributes:
        schema (FlowSchema):
        steps (list[FlowStep]):
        name (str | Unset):
        vars_ (list[FlowVar] | Unset):
    """

    schema: FlowSchema
    steps: list[FlowStep]
    name: str | Unset = UNSET
    vars_: list[FlowVar] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema = self.schema.value

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        name = self.name

        vars_: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.vars_, Unset):
            vars_ = []
            for vars_item_data in self.vars_:
                vars_item = vars_item_data.to_dict()
                vars_.append(vars_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema": schema,
                "steps": steps,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if vars_ is not UNSET:
            field_dict["vars"] = vars_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.flow_step import FlowStep
        from ..models.flow_var import FlowVar

        d = dict(src_dict)
        schema = FlowSchema(d.pop("schema"))

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = FlowStep.from_dict(steps_item_data)

            steps.append(steps_item)

        name = d.pop("name", UNSET)

        _vars_ = d.pop("vars", UNSET)
        vars_: list[FlowVar] | Unset = UNSET
        if _vars_ is not UNSET:
            vars_ = []
            for vars_item_data in _vars_:
                vars_item = FlowVar.from_dict(vars_item_data)

                vars_.append(vars_item)

        flow = cls(
            schema=schema,
            steps=steps,
            name=name,
            vars_=vars_,
        )

        flow.additional_properties = d
        return flow

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
