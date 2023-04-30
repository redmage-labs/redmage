from redmage.triggers import (
    DelayTriggerModifier,
    FromTriggerModifier,
    RootTriggerModifier,
    ThresholdTriggerModifier,
    ThrottleTriggerModifier,
    Trigger,
    TriggerModifier,
)
from redmage.types import HTMXTriggerModifier


def test_trigger():
    trigger = Trigger("click")
    assert trigger.create_trigger() == "click"


def test_trigger_to_string():
    trigger = Trigger("click")
    assert str(trigger) == "click"


def test_trigger_filter():
    trigger = Trigger("click", filter="test")
    assert trigger.create_trigger() == "click[test]"


def test_trigger_modifier_with_no_argument():
    modifier = TriggerModifier(HTMXTriggerModifier.CHANGED)
    assert modifier.create_modifier() == "changed"


def test_trigger_modifier():
    trigger = Trigger(
        "click", TriggerModifier(HTMXTriggerModifier.DELAY, milliseconds=100)
    )
    assert trigger.create_trigger() == "click delay:100ms"


def test_delay_trigger_modifier():
    modifier = DelayTriggerModifier(100)
    assert modifier.create_modifier() == "delay:100ms"


def test_throttle_trigger_modifier():
    modifier = ThrottleTriggerModifier(100)
    assert modifier.create_modifier() == "throttle:100ms"


def test_from_trigger_modifier():
    modifier = FromTriggerModifier("test")
    assert modifier.create_modifier() == "from:test"


def test_root_trigger_modifier():
    modifier = RootTriggerModifier("test")
    assert modifier.create_modifier() == "root:test"


def test_threshold_trigger_modifier():
    modifier = ThresholdTriggerModifier(0.5)
    assert modifier.create_modifier() == "threshold:0.5"
