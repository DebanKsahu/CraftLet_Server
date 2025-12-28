from typing import Annotated

from bson import ObjectId
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[
    ObjectId,
    BeforeValidator(
        lambda value: ObjectId(value) if not isinstance(value, ObjectId) else value
    ),
]
