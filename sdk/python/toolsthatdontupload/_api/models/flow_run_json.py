from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow import Flow
    from ..models.flow_run_json_vars import FlowRunJsonVars
    from ..models.input_file import InputFile


T = TypeVar("T", bound="FlowRunJson")


@_attrs_define
class FlowRunJson:
    """
    Attributes:
        flow (Flow): A saved flow (ttdu.flow/v1).
        files (list[InputFile]):
        vars_ (FlowRunJsonVars | Unset):
    """

    flow: Flow
    files: list[InputFile]
    vars_: FlowRunJsonVars | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flow = self.flow.to_dict()

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        vars_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.vars_, Unset):
            vars_ = self.vars_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flow": flow,
                "files": files,
            }
        )
        if vars_ is not UNSET:
            field_dict["vars"] = vars_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.flow import Flow
        from ..models.flow_run_json_vars import FlowRunJsonVars
        from ..models.input_file import InputFile

        d = dict(src_dict)
        flow = Flow.from_dict(d.pop("flow"))

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = InputFile.from_dict(files_item_data)

            files.append(files_item)

        _vars_ = d.pop("vars", UNSET)
        vars_: FlowRunJsonVars | Unset
        if isinstance(_vars_, Unset):
            vars_ = UNSET
        else:
            vars_ = FlowRunJsonVars.from_dict(_vars_)

        flow_run_json = cls(
            flow=flow,
            files=files,
            vars_=vars_,
        )

        flow_run_json.additional_properties = d
        return flow_run_json

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
