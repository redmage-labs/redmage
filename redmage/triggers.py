from typing import Optional

from redmage.types import HTMXTriggerModifier


class TriggerModifier:
    def __init__(
        self,
        modifier: str,
        milliseconds: Optional[int] = None,
        selector: Optional[str] = None,
        threshold: Optional[float] = None,
    ):
        self.modifier = modifier
        self.milliseconds = milliseconds
        self.selector = selector
        self.threshold = threshold

    def create_modifier(self) -> str:
        if self.milliseconds:
            return f"{self.modifier}:{self.milliseconds}ms"
        if self.threshold:
            return f"{self.modifier}:{self.threshold}"
        if self.selector:
            return f"{self.modifier}:{self.selector}"
        return self.modifier

    def __str__(self) -> str:
        return self.create_modifier()


class DelayTriggerModifier(TriggerModifier):
    def __init__(self, milliseconds: int):
        super().__init__(HTMXTriggerModifier.DELAY, milliseconds=milliseconds)


class ThrottleTriggerModifier(TriggerModifier):
    def __init__(self, milliseconds: int):
        super().__init__(HTMXTriggerModifier.THROTTLE, milliseconds=milliseconds)


class FromTriggerModifier(TriggerModifier):
    def __init__(self, selector: str):
        super().__init__(HTMXTriggerModifier.FROM, selector=selector)


class RootTriggerModifier(TriggerModifier):
    def __init__(self, selector: str):
        super().__init__(HTMXTriggerModifier.ROOT, selector=selector)


class ThresholdTriggerModifier(TriggerModifier):
    def __init__(self, threshold: float):
        super().__init__(HTMXTriggerModifier.THRESHHOLD, threshold=threshold)


class Trigger:
    def __init__(
        self, type: str, *modifiers: TriggerModifier, filter: Optional[str] = None
    ):
        self.type = type
        self.modifiers = modifiers
        self.filter = filter

    def create_trigger(self) -> str:
        trigger = self.type
        if self.filter:
            trigger += f"[{self.filter}]"

        if self.modifiers:
            return f"{trigger} {' '.join([str(m) for m in self.modifiers])}"
        return trigger

    def __str__(self) -> str:
        return self.create_trigger()
