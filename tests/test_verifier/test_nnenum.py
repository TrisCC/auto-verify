from pathlib import Path

import pytest
from result import Err, Ok

from autoverify.verifier import Nnenum

from .conftest import VerificationInstance

# from tests.util import run_av_cli


@pytest.fixture
def nnenum() -> Nnenum:
    return Nnenum()


@pytest.mark.install
def test_sat(nnenum: Nnenum, trivial_sat: VerificationInstance):
    result = nnenum.verify_property(trivial_sat.property, trivial_sat.network)

    assert isinstance(result, Ok)
    assert result.value.result == "SAT"


@pytest.mark.install
def test_unsat(nnenum: Nnenum, trivial_unsat: VerificationInstance):
    result = nnenum.verify_property(
        trivial_unsat.property, trivial_unsat.network
    )

    assert isinstance(result, Ok)
    assert result.value.result == "UNSAT"


@pytest.mark.install
def test_err(nnenum: Nnenum):
    result = nnenum.verify_property(Path(), Path())

    assert isinstance(result, Err)
