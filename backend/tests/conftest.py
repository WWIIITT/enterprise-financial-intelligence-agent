import pytest


@pytest.fixture(autouse=True)
def disable_qdrant_for_unit_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.rag.vector_store.settings.testing", True)
