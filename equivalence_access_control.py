# Access Group Classification based on User Attributes
from typing import List, Dict, Tuple
from collections import defaultdict
import csv

class User:
    def __init__(self, uid, name, dept, role, clearance):
        self.uid = uid
        self.name = name
        self.dept = dept.strip().lower()
        self.role = role.strip().lower()
        self.clearance = clearance.strip().lower()

    def attr_tuple(self) -> Tuple[str, str, str]:
        return (self.dept, self.role, self.clearance)

    def __repr__(self):
        return f"{self.uid}: {self.name} ({self.dept}, {self.role}, {self.clearance})"

def build_classes(users: List[User]) -> Dict[Tuple[str, str, str], List[User]]:
    groups = defaultdict(list)
    for u in users:
        groups[u.attr_tuple()].append(u)
    return dict(groups)

def check_reflexive(users: List[User], groups: Dict[Tuple[str,str,str], List[User]]) -> bool:
    for u in users:
        if u not in groups.get(u.attr_tuple(), []):
            return False
    return True

def check_sym_trans(users: List[User]) -> Tuple[bool, bool]:
    # equality-based relation -> symmetric & transitive true
    return True, True

def assign_permissions(groups: Dict[Tuple[str,str,str], List[User]]) -> Dict[Tuple[str,str,str], str]:
    perms = {}
    for key in groups:
        clr = key[2]
        if clr in ("high", "top", "3", "level3"):
            perms[key] = "Level 3 Access"
        elif clr in ("medium", "2", "level2"):
            perms[key] = "Level 2 Access"
        else:
            perms[key] = "Level 1 Access"
    return perms

def print_groups(groups: Dict[Tuple[str,str,str], List[User]], perms: Dict[Tuple[str,str,str], str]):
    print("\n--- Access Groups ---")
    g = 1
    for key, members in groups.items():
        dept, role, clr = key
        perm_text = perms.get(key, "Level ? (not assigned)")
        print(f"\nGroup {g}: {dept.title()}, {role.title()}, {clr.title()} -> {perm_text}")
        for u in members:
            print(f" - {u}")
        g += 1

def add_user_interactive(next_uid: int, users: List[User], groups: Dict[Tuple[str,str,str], List[User]]):
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return None
    dept = input("Department: ").strip() or "unknown"
    role = input("Role: ").strip() or "staff"
    clearance = input("Clearance (low/medium/high): ").strip() or "low"
    u = User(next_uid, name, dept, role, clearance)
    key = u.attr_tuple()
    if key in groups:
        groups[key].append(u)
        print(f"Added to existing group {key}.")
    else:
        groups[key] = [u]
        print(f"Created new group {key}.")
    users.append(u)
    return u

def list_users(users: List[User]):
    print("\n--- Users ---")
    for u in users:
        print(f" - {u}")

def show_user_ids(users: List[User]):
    print("\n--- User IDs ---")
    for u in users:
        print(f"{u.uid} -> {u.name}")

def save_groups_csv(groups: Dict[Tuple[str,str,str], List[User]], filename="groups_output.csv"):
    with open(filename, "w", newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["group_dept", "group_role", "group_clearance", "user_id", "user_name"])
        for key, members in groups.items():
            dept, role, clr = key
            for u in members:
                w.writerow([dept, role, clr, u.uid, u.name])
    print(f"Saved groups to {filename}")

def demo_data() -> List[User]:
    return [
        User(1, "Alice Smith", "Engineering", "Developer", "High"),
        User(2, "Bob Jones", "Engineering", "Developer", "High"),
        User(3, "Charlie Ray", "Engineering", "Tester", "Medium"),
        User(4, "Diana King", "HR", "Manager", "High"),
        User(5, "Eve Stone", "HR", "Manager", "High"),
        User(6, "Frank Liu", "Finance", "Analyst", "Low"),
        User(7, "Grace Y", "Engineering", "Developer", "High"),
        User(8, "Hector Z", "Finance", "Analyst", "Low"),
    ]

def main():
    print("Access Group Classification - Interactive")
    users = demo_data()
    groups = build_classes(users)
    perms = assign_permissions(groups)
    next_uid = max(u.uid for u in users) + 1

    while True:
        print("\nMenu:")
        print("1. List users")
        print("2. Show groups")
        print("3. Add user")
        print("4. Check relation properties")
        print("5. Save groups to CSV")
        print("6. Recompute groups/permissions")
        print("7. Show user IDs")
        print("8. Exit")
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            list_users(users)
        elif choice == "2":
            perms = assign_permissions(groups)
            print_groups(groups, perms)
        elif choice == "3":
            new_u = add_user_interactive(next_uid, users, groups)
            if new_u:
                next_uid += 1
                perms = assign_permissions(groups)
        elif choice == "4":
            print("\nRelation checks:")
            print("Reflexive:", check_reflexive(users, groups))
            s, t = check_sym_trans(users)
            print("Symmetric:", s)
            print("Transitive:", t)
        elif choice == "5":
            fn = input("Filename (default groups_output.csv): ").strip() or "groups_output.csv"
            save_groups_csv(groups, fn)
        elif choice == "6":
            groups = build_classes(users)
            perms = assign_permissions(groups)
            print("Recomputed groups and permissions.")
        elif choice == "7":
            show_user_ids(users)
        elif choice == "8":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
