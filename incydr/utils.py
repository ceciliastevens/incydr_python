from __future__ import annotations

from csv import DictReader
from csv import DictWriter
from io import IOBase
from itertools import chain
from itertools import repeat
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Generator
from typing import Iterable
from typing import List
from typing import TextIO
from typing import Tuple
from typing import Type
from typing import Union

from pydantic import BaseModel
from pydantic import ValidationError
from pydantic.fields import ModelField
from pydantic.fields import SHAPE_SINGLETON
from rich.console import ConsoleRenderable
from rich.console import Group
from rich.console import group
from rich.panel import Panel
from rich.text import Text


def get_field_value_and_info(
    model: BaseModel, path: List[str]
) -> Tuple[Any, ModelField]:
    """
    Traverse a pydantic model and its sub-models to retrieve both the value and `ModelField` data for a given attribute
    path.

    For example, given the following model hierarchy:

        class Child(BaseModel):
            field_1: str = Field("example", extra_data=1)
            field_2: int = Field(1)

        class Parent(BaseModel):
            field: str = Field("default")
            child: Child


    >>> model = Parent(child=Child())
    >>> value, field = get_field_value_and_info(model, path=["child", "field_1"])

    The `value` var would contain the string "example", and `field` would be the Field object for `Child.field_1`, where
    the 'extra_data' would be accessible in `field.field_info.extra`.
    """
    for p in path[:-1]:
        next_model = getattr(model, p)
        # if a child model is Optional and _not_ present, we can inspect the parent field data to get the missing child
        # class and use that to "construct" an empty version of the model, so child fields will still return valid
        # field_info, but the value will be `None` for every field on "missing" child models.
        if next_model is None:
            model_type = model.__fields__[p].type_
            model = model_type.construct(
                **{field: None for field in model_type.__fields__}
            )
        else:
            model = next_model
    value = getattr(model, path[-1])
    field = model.__fields__.get(path[-1])
    return value, field


def iter_model_formatted(
    model: BaseModel,
    include: List[str] = None,
    flat: bool = False,
    render: str = None,
):
    """
    Iterates through the fields of a Model (with optional flattening of sub-models), yielding (name, value) pairs.

    Accepts a list of field names to filter by (if flat=True, `include` list must be flattened dot-notation names).

    Will automatically attempt to "render" the field values in the following order:
       - if `render` arg is a string, it will look in the "extra" section of the pydantic model's Field Info for that
          name (expects a callable to be there)
       - if value is of a type that the model has a `json_encoder` for, it will use that encoder
       - otherwise will leave the value unchanged
    """
    fields = get_fields(model.__class__, include=include, flat=flat)
    for name in fields:
        path = name.split(".")
        value, field = get_field_value_and_info(model, path)
        field_renderer = None if not field else field.field_info.extra.get(render)
        if render and field_renderer:
            value = field_renderer(value)
            yield name, value
            continue
        json_encoder = model.Config.json_encoders.get(type(value))
        if json_encoder:
            value = json_encoder(value)
        yield name, value


def list_as_panel(items, sep=None, title=None, expand=True) -> Panel:
    """
    Renders a list of items as a `rich.panel.Panel`. If `sep` is provided will add a separator between each item (useful
    for rendering list of models that have multiple values.

    Examples:
        >>> from rich import print
        >>> print(list_as_panel(["one", "two", "three", "four"]))
        ╭───────╮
        │ one   │
        │ two   │
        │ three │
        │ four  │
        ╰───────╯

        >>> print(list_as_panel(["one", "two", "three", "four"], sep="---", title="example"))
        ╭─ example ─╮
        │ one       │
        │ ---       │
        │ two       │
        │ ---       │
        │ three     │
        │ ---       │
        │ four      │
        ╰───────────╯
    """
    if sep:
        items = list(chain(*zip(items, repeat(sep))))[:-1]
    return Panel(Group(*items), title=title, expand=expand)


@group()
def model_as_card(model):
    """
    Renders a pydantic model in 'card' format, where field name/value pairs are presented vertically, and when a field
    is a list of items, it renders it as a separate panel.
    """
    for name, value in iter_model_formatted(model, flat=True, render="table"):
        # rendering list fields takes some special handling
        if isinstance(value, list):
            if not len(value):
                yield f"{name}: []"
            # since a list of models can contain many values for each "item" in the list, we want to wrap the models
            # with a separator to make it readable and easily distinguish where each model begins/ends.
            elif isinstance(value[0], BaseModel):
                yield list_as_panel(
                    [model_as_card(v) for v in value], title=name, sep="---"
                )
            else:
                yield list_as_panel(value, title=name)
        # this should only be true when a model field has a "table" extra renderer defined
        elif isinstance(value, ConsoleRenderable):
            yield Panel.fit(value, title=name)
        else:
            yield Text(f"{name}: {value}", overflow="fold")


def flatten_fields(model: Type[BaseModel]) -> Generator[str, None, None]:
    """
    Yields all fields of a model and any sub-models as flat, dot-notation strings.

    For example, given the following model hierarchy:

        class Child(BaseModel):
            field_1: str
            field_2: int

        class Parent(BaseModel):
            field: str
            child: Child

    flatten_fields(Parent) would yield: ['field', 'child.field_1', 'child.field_2']
    """
    for name, field in model.__fields__.items():
        # the field.shape tells us if the field contains a single `BaseModel` or something like a `List[BaseModel]`
        # we can only traverse singleton models when flattening
        if issubclass(field.type_, BaseModel) and field.shape == SHAPE_SINGLETON:
            for child_name in flatten_fields(field.type_):
                yield f"{name}.{child_name}"
        else:
            yield name


def get_fields(
    model: Type[BaseModel], include: List[str] = None, flat: bool = False
) -> Generator[str, None, None]:
    """
    Yields fields from a model.

    If flat=True will flatten nested models.

    Results can be filtered with `include` param list. Values can either be the field name, or a wildcard name which
    will include subfields matching that name pattern. For example: ["event.id", "file.*"] will yield the event.id
    field and _all_ file fields of the nested FileEventV2 model.

    Order is preserved to match `include` order, to allow precise table/csv column ordering based on user input.
    """
    fields = list(flatten_fields(model)) if flat else model.__fields__
    if not include:
        yield from fields
    else:
        for i in include:
            found = False
            if "*" in i:
                pattern = i.replace("*", "")
                for f in fields:
                    if f.startswith(pattern):
                        found = True
                        yield f
            elif i in fields:
                found = True
                yield i
            if not found:
                raise ValueError(
                    f"'{i}' is not a valid field path for model: {model.__name__}",
                    list(fields),
                )


class CSVValidationError(Exception):
    def __init__(self, msg, row):
        self.msg = msg
        self.row = row

    def __str__(self):
        return self.msg


def read_models_from_csv(
    model: Type[BaseModel], path: Union[str, Path, IOBase]
) -> Generator[BaseModel, None, None]:
    if isinstance(path, IOBase):
        file = path
    else:
        path = Path(path)
        file = path.open(mode="r", encoding="utf-8")
    reader = DictReader(file)

    error = None
    for row in reader:
        for key, val in row.items():
            if val == "":
                row[key] = None
        try:
            yield model(**row)  # noqa
        except ValidationError as err:
            error = CSVValidationError(
                f"Bad data in row {reader.line_num} of {path}\n{str(err)}",
                row=reader.line_num,
            )
    if error:
        raise error


def read_dict_from_csv(
    path: Union[str, Path, IOBase], field_names: List[str] = None
) -> Generator[dict, None, None]:
    if isinstance(path, IOBase):
        file = path
    else:
        path = Path(path)
        file = path.open(mode="r", encoding="utf-8")
    reader = DictReader(file, fieldnames=field_names)
    for row in reader:
        for key, val in row.items():
            if val == "":
                row[key] = None
        yield row  # noqa


def write_models_to_csv(
    models: Iterable[BaseModel],
    path: Union[str, Path, IOBase, TextIO],
    columns: List[str] = None,
):
    if columns:
        columns = set(columns)
    if isinstance(path, IOBase):
        file = path
    else:
        path = Path(path)
        file = path.open(mode="w", encoding="utf-8")
    models = iter(models)
    first = next(models)
    writer = DictWriter(file, fieldnames=list(first.__fields__))
    writer.writeheader()
    for model in chain([first], models):
        writer.writerow(model.dict(by_alias=False, include=columns))


def write_dict_to_csv(
    models: List[Dict],
    path: Union[str, Path, IOBase, TextIO] = None,
    columns: str = None,
):
    if columns:
        columns = [c.strip() for c in columns.split(",")]

    models = iter(models)
    first = next(models)

    if columns:
        first = {c: first[c] for c in columns}
    first = flatten_fields(first)

    if isinstance(path, IOBase):
        file = path
    else:
        path = Path(path)
        file = path.open(mode="w", encoding="utf-8")

    writer = DictWriter(file, fieldnames=list(first.keys()))
    writer.writeheader()
    for model in chain([first], models):
        if columns:
            model = {c: model[c] for c in columns}
        writer.writerow(flatten_fields(model))
