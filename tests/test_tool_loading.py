from tools import BaseTool, load_all_tools


def test_all_tools_load():
    tools = load_all_tools()

    assert "respond" in tools
    assert "image" in tools
    assert "sysmon" in tools
    assert "regex" in tools
    assert "archive" in tools
    assert "datetime" in tools
    assert "hash" in tools
    assert "project_inspector" in tools
    assert len(tools) >= 36

    for name, tool in tools.items():
        assert isinstance(tool, BaseTool), name
        assert tool.name == name
        assert tool.description
        assert tool.usage_example


def test_regex_presets_smoke():
    tools = load_all_tools()

    result = tools["regex"].run("extract email | Contact hello@example.com")

    assert "hello@example.com" in result


def test_hash_text_smoke():
    tools = load_all_tools()

    result = tools["hash"].run("text sha256 cortex")

    assert "sha256:" in result
    assert "1ee11af4ed5d63caf142a30a96ba124b1dde039d93b15b69858251295d4a92a6" in result


def test_datetime_add_smoke():
    tools = load_all_tools()

    result = tools["datetime"].run("add 2026-05-04T00:00:00+00:00 | 1")

    assert result.startswith("2026-05-05T00:00:00+00:00")


def test_project_inspector_summary_smoke():
    tools = load_all_tools()

    result = tools["project_inspector"].run("summary .")

    assert "Files" in result
    assert ".py" in result
