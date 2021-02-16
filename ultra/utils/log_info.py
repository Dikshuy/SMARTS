import math


class LogInfo:
    def __init__(self):
        self.data = {
            "env_score": 0,
            "episode_reward": 0,
            "dist_center": 0,
            "goal_dist": 0,
            "speed": 0,
            "max_speed_violation": 0,
            "ego_num_violations": 0,
            "social_num_violations": 0,
            "ego_linear_jerk": 0.0,
            "ego_angular_jerk": 0.0,
            "final_pos": [0, 0],
            "start_pos": [0, 0],
            "dist_travelled": 0.0,
            "collision": 0,
            "off_road": 0,
            "off_route": 0,
            "reached_goal": 0,
            "timed_out": 0,
            "episode_length": 0,
        }

    def add(self, infos, rewards):

        self.data["env_score"] += int(infos["logs"]["env_score"])
        self.data["speed"] += infos["logs"]["speed"]
        self.data["max_speed_violation"] += (
            1 if infos["logs"]["speed"] > infos["logs"]["closest_wp"].speed_limit else 0
        )
        self.data["dist_center"] += infos["logs"]["dist_center"]
        self.data["ego_num_violations"] += int(infos["logs"]["ego_num_violations"] > 0)
        self.data["social_num_violations"] += int(
            infos["logs"]["social_num_violations"] > 0
        )
        self.data["goal_dist"] = infos["logs"]["goal_dist"]
        self.data["ego_linear_jerk"] += infos["logs"]["linear_jerk"]
        self.data["ego_angular_jerk"] += infos["logs"]["angular_jerk"]
        self.data["episode_reward"] += rewards
        self.data["final_pos"] = infos["logs"]["position"]
        self.data["start_pos"] = infos["logs"]["start"].position
        self.data["dist_travelled"] = math.sqrt(
            (self.data["final_pos"][1] - self.data["start_pos"][1]) ** 2
            + (self.data["final_pos"][0] - self.data["start_pos"][0]) ** 2
        )
        # recording termination cases
        events = infos["logs"]["events"]
        self.data["collision"] = (
            False
            if len(events.collisions) == 0 or events.collisions[0].collidee_id == 0
            else True
        )
        self.data["off_road"] = int(events.off_road)
        self.data["off_route"] = int(events.off_route)
        self.data["reached_goal"] = int(events.reached_goal)
        self.data["timed_out"] = int(events.reached_max_episode_steps)
        #

    def normalize(self, steps):
        self.data["env_score"] /= steps
        self.data["dist_center"] /= steps
        self.data["episode_length"] = steps
        self.data["speed"] /= steps
        self.data["ego_linear_jerk"] /= steps
        self.data["ego_angular_jerk"] /= steps
        self.data["ego_num_violations"] /= steps
        self.data["social_num_violations"] /= steps
        self.data["max_speed_violation"] /= steps
