class Draven:
    def __init__(self, level, items, enemy_armor):
        self.base_ad = 62
        self.ad_growth = 3.6
        self.base_as = 0.679
        self.as_growth = 0.027
        self.level = level
        self.items = items
        self.enemy_armor = enemy_armor
        self.total_ad = self.calculate_total_stat(self.base_ad, self.ad_growth, 'ad')
        self.crit_chance = self.calculate_crit_chance()
        self.crit_damage_multiplier = self.calculate_crit_damage_multiplier()
        self.total_as = self.calculate_total_stat(self.base_as, self.as_growth, 'attack_speed')
        self.lethality = self.calculate_lethality()
        self.armor_pen = self.calculate_armor_pen()

    def calculate_total_stat(self, base, growth, stat_type):
        level_ups = self.level - 1
        if stat_type == 'ad':
            bonus = sum(item.get('ad', 0) for item in self.items)
        elif stat_type == 'attack_speed':
            bonus = sum(item.get('attack_speed', 0) for item in self.items)
        else:
            bonus = 0
        return base + bonus + growth * level_ups * (0.7025 + 0.0175 * level_ups)

    def calculate_crit_chance(self):
        return sum(item.get('crit_chance', 0) for item in self.items)

    def calculate_crit_damage_multiplier(self):
        base_crit_damage = 1.75  # Normal crits deal 175% damage
        additional_crit_damage = sum(item.get('crit_damage', 0) for item in self.items)
        return base_crit_damage + additional_crit_damage

    def calculate_lethality(self):
        return sum(item.get('lethality', 0) for item in self.items)

    def calculate_armor_pen(self):
        return sum(item.get('armor_pen', 0) for item in self.items)

    def calculate_effective_armor(self):
        # Calculate the effective armor after applying lethality and armor penetration
        # lethality_reduction = self.lethality * (0.6 + 0.4 * (self.level / 18))
        effective_armor = self.enemy_armor #- lethality_reduction
        effective_armor *= (1 - self.armor_pen)
        effective_armor -= self.lethality
        return max(effective_armor, 0)  # Armor cannot go below 0

    def calculate_q_damage(self, crit=False):
        q_bonus_physdmg, q_bonus_percentage = 40, 0.75  # Level 1 Qself.total_ad
        if self.level >= 4:
            q_bonus_physdmg += 5
            q_bonus_percentage += 0.1
        if self.level >= 5:
            q_bonus_physdmg += 5
            q_bonus_percentage += 0.1
        if self.level >= 7:
            q_bonus_physdmg += 5
            q_bonus_percentage += 0.1
        if self.level >= 9: # Q Max
            q_bonus_physdmg += 5
            q_bonus_percentage += 0.1
        bonus = sum(item.get('ad', 0) for item in self.items)
        base = self.total_ad - bonus
        base_damage = base + bonus * (1 + q_bonus_percentage) + q_bonus_physdmg
        effective_armor = self.calculate_effective_armor()
        damage_reduction = 100 / (100 + effective_armor)
        if crit:
            # print(self.crit_damage_multiplier)
            # print(damage_reduction)
            # print(base_damage)
            return (self.total_ad * self.crit_damage_multiplier + bonus * q_bonus_percentage + q_bonus_physdmg) * damage_reduction 
        else:
            return base_damage * damage_reduction

    def calculate_dps(self, duration=30):
        non_crit_damage = self.calculate_q_damage(crit=False)
        crit_damage = self.calculate_q_damage(crit=True)
        average_damage_per_hit = (
            non_crit_damage * (1 - self.crit_chance) + crit_damage * self.crit_chance
        )
        attacks_per_second = self.total_as
        total_attacks = attacks_per_second * duration
        total_damage = average_damage_per_hit * total_attacks
        dps = total_damage / duration
        return dps, total_damage

    def display_damage(self):
        normal_damage = self.calculate_q_damage(crit=False)
        crit_damage = self.calculate_q_damage(crit=True)
        dps, total_damage = self.calculate_dps()
        print(f"Normal Q damage: {normal_damage:.2f}")
        print(f"Crit Q damage: {crit_damage:.2f}")
        print(f"DPS over 30 seconds: {dps:.2f}")
        print(f"Total damage over 30 seconds: {total_damage:.2f}")

# Example items data
items = [

    {"name": "Runes", "ad": 5},
    # {"name": "Zephyr", "attack_speed": 0.45},
    {"name": "Berserker's Greaves", "attack_speed": 0.35},
    {"name": "Bloodthirster", "ad": 80},
    {"name": "Infinity Edge", "ad": 80, "crit_chance": 0.25, "crit_damage": 0.40},
    # {"name": "Immortal Shieldbow", "ad": 55, "crit_chance": 0.25},
    # # {"name": "Essence Reaver", "ad": 70, "crit_chance": 0.25},
    {"name": "The Collector", "ad": 60, "crit_chance": 0.25, "lethality": 12},
    # {"name": "Lord Dominik's Regards", "ad": 45, "crit_chance": 0.25, "armor_pen": 0.4},
]

# Item list = [
#     {"name": "Kraken Slayer", "ad": 65, "crit_chance": 0.20, "attack_speed": 0.25},
#     {"name": "Zephyr", "attack_speed": 0.45}
#     {"name": "Phantom Dancer", "ad": 20, "crit_chance": 0.25, "attack_speed": 0.45},
# ]

draven = Draven(level=6, items=items, enemy_armor=50)
draven.display_damage()
