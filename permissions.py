from dataclasses import dataclass

@dataclass
class Permissions:
    can_review: bool
    can_approve: bool
    can_edit: bool