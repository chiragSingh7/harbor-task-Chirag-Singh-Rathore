import json
from pathlib import Path

OUTPUT_PATH = Path("/app/output.json")

EXPECTED_REPORT = [
    {
        "service": "api",
        "windows": [[50, 100], [120, 150]],
        "total_minutes": 80,
        "longest_minutes": 50,
    },
    {
        "service": "web",
        "windows": [[0, 40], [60, 90]],
        "total_minutes": 70,
        "longest_minutes": 40,
    },
]


def _read_output() -> list[dict]:
    return json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))


def test_output_file_exists():
    assert OUTPUT_PATH.exists(), f"Missing output file: {OUTPUT_PATH}"


def test_output_is_a_json_array():
    assert isinstance(_read_output(), list)


def test_only_services_with_approved_windows_are_included():
    services = [item["service"] for item in _read_output()]
    assert services == ["api", "web"]
    assert "worker" not in services


def test_overlapping_and_touching_windows_are_merged():
    by_service = {item["service"]: item for item in _read_output()}
    assert by_service["web"]["windows"][0] == [0, 40]
    assert by_service["api"]["windows"][0] == [50, 100]


def test_disjoint_windows_remain_separate():
    by_service = {item["service"]: item for item in _read_output()}
    assert by_service["api"]["windows"] == [[50, 100], [120, 150]]
    assert by_service["web"]["windows"] == [[0, 40], [60, 90]]


def test_duration_metrics_use_merged_windows():
    by_service = {item["service"]: item for item in _read_output()}
    assert by_service["api"]["total_minutes"] == 80
    assert by_service["api"]["longest_minutes"] == 50
    assert by_service["web"]["total_minutes"] == 70
    assert by_service["web"]["longest_minutes"] == 40


def test_output_schema_has_no_extra_fields():
    required_keys = {"service", "windows", "total_minutes", "longest_minutes"}
    assert all(set(item) == required_keys for item in _read_output())


def test_complete_report_matches_expected_result():
    assert _read_output() == EXPECTED_REPORT


def test_pretty_printed_with_trailing_newline():
    text = OUTPUT_PATH.read_text(encoding="utf-8")
    assert text.endswith("\n")
    assert text == json.dumps(json.loads(text), indent=2) + "\n"
