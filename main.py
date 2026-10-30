from setting_manager.local_requirement_collector import LocalRequirementCollector

LRC = LocalRequirementCollector()
print(LRC.find_requirement_names())
print("-" * 20)
print(LRC.find_requirement_values())
print("-" * 20)
print(LRC.new_requirement({"1": "2"}))
print(LRC.find_requirement_values())
