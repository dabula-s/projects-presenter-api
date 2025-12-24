from typing import Protocol
from typing import TypeVar

T_Input = TypeVar('T_Input', contravariant=True)
T_Output = TypeVar('T_Output', covariant=True)


class Service(Protocol[T_Input, T_Output]):

    def call(self, dto: T_Input) -> T_Output: ...
