from abc import ABC
from typing import Type, Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: Type[Any]) -> Any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected an int, got {type(value)}")

        if value not in range(self.min_amount, self.max_amount + 1):
            raise ValueError(
                f"Value must be between "
                f"{self.min_amount} and {self.max_amount}"
            )

        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.protected_name = f"_{name}"


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
        except TypeError as e:
            print(
                f"{visitor.name} can't access, "
                f"has an attribute with incorrect type!",
                e
            )
        except ValueError as e:
            print(
                f"{visitor.name} can't access, "
                f"doesn't meet the requirements!",
                e
            )
        else:
            return True

        return False
