from typing import Dict, Set

class GroupManager:
    def __init__(self):
        self.groups: Dict[str, Set[str]] = {}

    def create_group(self, group_name: str):
        self.groups.setdefault(group_name, set())

    def delete_group(self, group_name: str):
        if group_name in self.groups:
            del self.groups[group_name]

    def add_to_group(self, group_name: str, client_id: str):
        self.groups.setdefault(group_name, set()).add(client_id)

    def remove_from_group(self, group_name: str, client_id: str):
        if group_name in self.groups:
            self.groups[group_name].discard(client_id)
            if not self.groups[group_name]:
                del self.groups[group_name]

    def get_group_members(self, group_name: str) -> Set[str]:
        return self.groups.get(group_name, set())

    def remove_connection(self, client_id: str):
        for group in list(self.groups):
            self.groups[group].discard(client_id)
            if not self.groups[group]:
                del self.groups[group]