"""Report generation utilities."""

import csv
import json
from pathlib import Path


class Reporter:
    def print_report(self, results, quiet=False):
        print(self._build_text_report(results, quiet=quiet))

    def save_report(self, results, output_path, output_format="json"):
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "json":
            path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
            return
        if output_format == "txt":
            path.write_text(self._build_text_report(results, quiet=True), encoding="utf-8")
            return
        if output_format == "csv":
            self._write_csv(results, path)
            return
        raise ValueError(f"Unsupported output format: {output_format}")

    def _build_text_report(self, results, quiet=False):
        lines = []
        for item in results:
            title = item.get("username") or item.get("email") or "target"
            target_type = item.get("target_type", "target")
            lines.append(f"[{target_type}] {title}")
            for key, value in item.items():
                if key in {"username", "email", "target_type"}:
                    continue
                lines.append(f"  {key}:")
                if isinstance(value, list):
                    if not value:
                        lines.append("    - none")
                        continue
                    for entry in value:
                        if isinstance(entry, dict):
                            summary = ", ".join(f"{k}={v}" for k, v in entry.items() if v not in (None, [], {}))
                            lines.append(f"    - {summary}")
                        else:
                            lines.append(f"    - {entry}")
                elif isinstance(value, dict):
                    if not value:
                        lines.append("    - none")
                    else:
                        for sub_key, sub_value in value.items():
                            lines.append(f"    - {sub_key}: {sub_value}")
                else:
                    lines.append(f"    - {value}")
            if not quiet:
                lines.append("")
        return "\n".join(lines).strip()

    def _write_csv(self, results, path):
        rows = []
        for item in results:
            target = item.get("username") or item.get("email")
            target_type = item.get("target_type", "target")
            for section, value in item.items():
                if section in {"username", "email", "target_type"}:
                    continue
                if isinstance(value, list):
                    for entry in value:
                        if isinstance(entry, dict):
                            row = {"target": target, "target_type": target_type, "section": section}
                            row.update(entry)
                            rows.append(row)
                        else:
                            rows.append({"target": target, "target_type": target_type, "section": section, "value": entry})
                elif isinstance(value, dict):
                    for key, sub_value in value.items():
                        rows.append({"target": target, "target_type": target_type, "section": section, "field": key, "value": sub_value})
                else:
                    rows.append({"target": target, "target_type": target_type, "section": section, "value": value})

        fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else ["target", "target_type", "section", "value"]
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
