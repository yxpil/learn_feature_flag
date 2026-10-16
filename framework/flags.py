"""Feature flags: toggle features on per user, percentage rollout, or env.
Code branches on the flag so new logic rolls out gradually."""
import hashlib


class FeatureFlags:
    def __init__(self):
        self.flags = {}  # name -> {"enabled": bool, "percentage": int, "users": set}

    def define(self, name, enabled=False, percentage=0, users=None):
        self.flags[name] = {
            "enabled": enabled,
            "percentage": percentage,
            "users": set(users or []),
        }

    def is_on(self, name, user_id=None):
        flag = self.flags.get(name)
        if not flag or not flag["enabled"]:
            return False
        if user_id and user_id in flag["users"]:
            return True
        if user_id and flag["percentage"] > 0:
            h = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
            return h % 100 < flag["percentage"]
        # enabled but no user targeting -> only on if explicitly all-on
        return flag.get("all_on", False)
