"""
Basic tests for the training pipeline.

These tests are intentionally lightweight:
- They verify that running the training pipeline produces
  a model file and a report file.
- This is enough to show engineering discipline and to
  integrate with CI later if desired.
"""

from pathlib import Path
import shutil

from sentinelflow.pipeline import run_training
from sentinelflow import config


def test_run_training_creates_artifacts(tmp_path: Path):
    """
    Run the training pipeline and ensure artifacts are created.

    In plain English:
    - Temporarily redirect the model/report paths to a temp folder.
    - Call run_training().
    - Check that the expected files exist.
    """

    # Backup original paths so we can restore them after the test.
    original_model_path = config.MODEL_PATH
    original_report_path = config.REPORT_PATH

    try:
        # Redirect output paths to the temporary directory pytest gives us.
        config.MODEL_PATH = tmp_path / "model.joblib"
        config.REPORT_PATH = tmp_path / "report.json"

        # Run the training pipeline end-to-end.
        run_training()

        # Check that the training actually produced files.
        assert config.MODEL_PATH.exists()
        assert config.REPORT_PATH.exists()

    finally:
        # Always restore original config paths to avoid side effects.
        config.MODEL_PATH = original_model_path
        config.REPORT_PATH = original_report_path

        # Clean up temporary artifacts if they still exist.
        if tmp_path.exists():
            shutil.rmtree(tmp_path)
