from tools import BaseTool, load_all_tools


def test_all_tools_load():
    tools = load_all_tools()

    assert "respond" in tools
    assert "image" in tools
    assert "sysmon" in tools
    assert "regex" in tools
    assert len(tools) >= 30

    for name, tool in tools.items():
        assert isinstance(tool, BaseTool), name
        assert tool.name == name
        assert tool.description
        assert tool.usage_example


def test_regex_presets_smoke():
    tools = load_all_tools()

    result = tools["regex"].run("extract email | Contact hello@example.com")

    assert "hello@example.com" in result
