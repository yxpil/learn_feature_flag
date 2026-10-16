"""Demo: feature flags - roll out a new checkout flow gradually."""
from framework.flags import FeatureFlags


def checkout(user_id, flags):
    if flags.is_on("new_checkout", user_id):
        return f"[{user_id}] -> new checkout flow"
    return f"[{user_id}] -> old checkout flow"


def main():
    flags = FeatureFlags()

    print("--- Case 1: flag off, everyone gets old flow ---")
    flags.define("new_checkout", enabled=False)
    for u in ["alice", "bob", "carol"]:
        print(" ", checkout(u, flags))

    print("\n--- Case 2: only alice in the allowlist ---")
    flags.define("new_checkout", enabled=True, users=["alice"])
    for u in ["alice", "bob", "carol"]:
        print(" ", checkout(u, flags))

    print("\n--- Case 3: 50% rollout (hash-based, consistent per user) ---")
    flags.define("new_checkout", enabled=True, percentage=50)
    for u in ["alice", "bob", "carol", "dave", "erin"]:
        print(" ", checkout(u, flags))

    print("\n== all cases done ==")


if __name__ == "__main__":
    main()
