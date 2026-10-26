"""Declarative YAML rule loader/evaluator."""
from pathlib import Path
import json, yaml
from jsonschema import Draft202012Validator
from .schemas import Verdict

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "rules" / "rules.schema.json"

class RuleEngine:
    def __init__(self, rules_dir):
        self.rules = []
        directory = Path(rules_dir)
        if not directory.is_dir():
            raise FileNotFoundError(directory)
        validator = Draft202012Validator(json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
        seen = set()
        for path in sorted(directory.glob("*.yaml")):
            with path.open(encoding="utf-8") as f:
                documents = list(yaml.safe_load_all(f))
            for index, rule in enumerate(documents, 1):
                if rule is None: continue
                errors = list(validator.iter_errors(rule))
                if errors:
                    raise ValueError(f"{path.name} document {index}: " + "; ".join(e.message for e in errors))
                if rule["rule_id"] in seen:
                    raise ValueError(f"duplicate rule_id: {rule['rule_id']}")
                seen.add(rule["rule_id"])
                self.rules.append(rule)

    def evaluate(self, event):
        return [self._verdict(rule) for rule in self.rules if self._matches(rule, event)]

    def _matches(self, rule, event):
        scope = rule.get("scope")
        if scope and not event.get("event_type", "").lower().startswith(scope.lower() + "_"):
            return False
        return all(self._resolve(key, event) == expected for key, expected in rule["when"].items())

    @staticmethod
    def _resolve(path, event):
        current = event
        for part in path.split("."):
            if not isinstance(current, dict) or part not in current:
                return None
            current = current[part]
        return current

    @staticmethod
    def _verdict(rule):
        then = rule["then"]
        return Verdict(
            rule_id=rule["rule_id"], verdict=then["verdict"],
            severity=then["severity"],
            epistemic=rule.get("epistemic", {}).get("verdict", "UNKNOWN"),
            evidence=then.get("evidence", []))
