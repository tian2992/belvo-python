import pytest

from belvo import resources


@pytest.mark.parametrize(
    ("method", "params"), [("resume", {"fake-token", "fake-session"}), ("delete", {"fake-token"})]
)
def test_institutions_raises_not_implemented(method, params, api_session):
    institutions = resources.Institutions(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(institutions, method)
        assert func(*params)
