"""reqdecide — calibrated requirement admission control.

Each stakeholder statement is a decision, not raw material for FR-xx generation:
admit it into the specification, ask one clarifying question, or block it, under
a limited question budget.

Method notes live in ``research/05-NOVEL-METHODS.md``; the validation ladder that
these modules feed lives in ``research/06-EVALUATION-FRAMEWORK.md``.
"""

from .policy import AdmissionProposal, CriticFlags, decide
from .schema import (
    Action,
    CostModel,
    Decision,
    DecisionLabel,
    Message,
    OrgRule,
    Project,
    Requirement,
    SuperClass,
    TurnInput,
    UncertaintySignal,
    super_class_of,
)

__version__ = "0.1.0"

__all__ = [
    "Action",
    "AdmissionProposal",
    "CostModel",
    "CriticFlags",
    "Decision",
    "DecisionLabel",
    "Message",
    "OrgRule",
    "Project",
    "Requirement",
    "SuperClass",
    "TurnInput",
    "UncertaintySignal",
    "__version__",
    "decide",
    "super_class_of",
]
