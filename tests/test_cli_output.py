from main import _prepare_stdout_text


def test_prepare_stdout_text_returns_original_when_short_enough() -> None:
    text = "Bao cao ngan"
    assert _prepare_stdout_text(text, max_chars=100) == text


def test_prepare_stdout_text_truncates_and_marks_output() -> None:
    text = "x" * 50
    output = _prepare_stdout_text(text, max_chars=20)

    assert len(output) == 20
    assert output.endswith("[truncated]")
