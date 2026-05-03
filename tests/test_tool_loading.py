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
    assert "encoding" in tools
    assert "markdown" in tools
    assert "random" in tools
    assert "url" in tools
    assert "diff" in tools
    assert "env_file" in tools
    assert "logs" in tools
    assert "sqlite" in tools
    assert len(tools) >= 44

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


def test_encoding_base64_smoke():
    tools = load_all_tools()

    assert tools["encoding"].run("base64-encode cortex") == "Y29ydGV4"
    assert tools["encoding"].run("base64-decode Y29ydGV4") == "cortex"


def test_url_parse_smoke():
    tools = load_all_tools()

    result = tools["url"].run("query https://example.com/search?q=cortex&tag=agent")

    assert '"q": [' in result
    assert "cortex" in result


def test_markdown_toc_smoke():
    tools = load_all_tools()

    result = tools["markdown"].run("toc # Title\n## Child")

    assert "[Title](#title)" in result
    assert "[Child](#child)" in result


def test_diff_text_smoke():
    tools = load_all_tools()

    result = tools["diff"].run("text hello | hello world")

    assert "+hello world" in result


def test_logs_errors_smoke():
    tools = load_all_tools()

    result = tools["logs"].run("errors INFO ok\nERROR failed to start")

    assert "failed to start" in result


def test_sqlite_tables_smoke():
    import sqlite3
    from pathlib import Path
    from uuid import uuid4

    tmp_dir = Path(".test-tmp")
    tmp_dir.mkdir(exist_ok=True)
    db_path = tmp_dir / f"sample-{uuid4().hex}.db"
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("create table users (id integer primary key, name text)")

        tools = load_all_tools()
        result = tools["sqlite"].run(f"tables {db_path}")

        assert "users" in result
    finally:
        try:
            db_path.unlink(missing_ok=True)
        except PermissionError:
            pass
