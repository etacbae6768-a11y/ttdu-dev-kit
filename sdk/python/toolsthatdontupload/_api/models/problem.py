from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.problem_details import ProblemDetails


T = TypeVar("T", bound="Problem")


@_attrs_define
class Problem:
    """
    Attributes:
        title (str):
        status (int):
        type_ (str | Unset):
        detail (str | Unset):
        code (str | Unset): invalid_input, needs_input, unsupported, resource_limit, browser_only, ...
        step (None | str | Unset):
        details (ProblemDetails | Unset):
    """

    title: str
    status: int
    type_: str | Unset = UNSET
    detail: str | Unset = UNSET
    code: str | Unset = UNSET
    step: None | str | Unset = UNSET
    details: ProblemDetails | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        status = self.status

        type_ = self.type_

        detail = self.detail

        code = self.code

        step: None | str | Unset
        if isinstance(self.step, Unset):
            step = UNSET
        else:
            step = self.step

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "status": status,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if detail is not UNSET:
            field_dict["detail"] = detail
        if code is not UNSET:
            field_dict["code"] = code
        if step is not UNSET:
            field_dict["step"] = step
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.problem_details import ProblemDetails

        d = dict(src_dict)
        title = d.pop("title")

        status = d.pop("status")

        type_ = d.pop("type", UNSET)

        detail = d.pop("detail", UNSET)

        code = d.pop("code", UNSET)

        def _parse_step(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        step = _parse_step(d.pop("step", UNSET))

        _details = d.pop("details", UNSET)
        details: ProblemDetails | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = ProblemDetails.from_dict(_details)

        problem = cls(
            title=title,
            status=status,
            type_=type_,
            detail=detail,
            code=code,
            step=step,
            details=details,
        )

        problem.additional_properties = d
        return problem

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
