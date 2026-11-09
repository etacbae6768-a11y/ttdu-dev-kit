from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_step_scope import FlowStepScope
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_step_options import FlowStepOptions


T = TypeVar("T", bound="FlowStep")


@_attrs_define
class FlowStep:
    """
    Attributes:
        tool (str):  Example: pdf.merge.
        scope (FlowStepScope | Unset): all = every file to the tool at once; each = one run per file
        options (FlowStepOptions | Unset):
        out_name (str | Unset): Output name template, e.g. "{client}-merged"
    """

    tool: str
    scope: FlowStepScope | Unset = UNSET
    options: FlowStepOptions | Unset = UNSET
    out_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tool = self.tool

        scope: str | Unset = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.value

        options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        out_name = self.out_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tool": tool,
            }
        )
        if scope is not UNSET:
            field_dict["scope"] = scope
        if options is not UNSET:
            field_dict["options"] = options
        if out_name is not UNSET:
            field_dict["outName"] = out_name

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.flow_step_options import FlowStepOptions

        d = dict(src_dict)
        tool = d.pop("tool")

        _scope = d.pop("scope", UNSET)
        scope: FlowStepScope | Unset
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = FlowStepScope(_scope)

        _options = d.pop("options", UNSET)
        options: FlowStepOptions | Unset
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = FlowStepOptions.from_dict(_options)

        out_name = d.pop("outName", UNSET)

        flow_step = cls(
            tool=tool,
            scope=scope,
            options=options,
            out_name=out_name,
        )

        flow_step.additional_properties = d
        return flow_step

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
