from pathlib import Path
from typing import Any

import pandas as pd

from upr_ai.utils.Exception import (
    DataReadError,
    DataValidationError,
    FileError,
)
from upr_ai.utils.logger import Logger


class DataLoader:
    """
    Handles data loading and validation only.
    """

    def __init__(
        self,
        file_path: str,
        request_id: str,
        user_id: str,
        logger_config: dict[Any, Any],
        logger_fallback_file: str,
        required_fields: dict[str, type],
    ):
        self.logger = Logger(
            request_id,
            user_id,
            name="Data Loader",
            config=logger_config,
            fall_back_log_file=logger_fallback_file,
        )
        self.logger.info("Initializing Data Loader...")
        self.file_path = Path(file_path)
        self.file_type = "csv"

        self.REQUIRED_FIELDS = required_fields

    def load(self) -> pd.DataFrame:
        """
        Load data from file and validate it.
        """
        data = self._read_file()
        self._validate(data)
        return data

    def _read_file(self) -> pd.DataFrame:
        """
        Read raw data from CSV .
        """
        try:
            if not self.file_path.exists():
                raise FileError(f"File not found: {self.file_path}")

            with self.file_path.open("r", encoding="utf-8") as file:
                return pd.read_csv(file)

        except FileError as exc:
            self.logger.error(f"File does not exist: {self.file_path}", exc=exc)
            raise DataReadError(
                f"File not found: {self.file_path}", original_exception=exc
            ) from exc

        except TypeError as exc:
            self.logger.error(f"Unsupported file type: {self.file_type}", exc=exc)
            raise DataReadError(
                f"Unsupported file type: {self.file_type}", original_exception=exc
            ) from exc

        except Exception as exc:
            self.logger.error(
                f"Unknown error while reading data file: {self.file_path}", exc=exc
            )
            raise DataReadError(
                f"Unknown error while reading data file: {self.file_path}",
                original_exception=exc,
            ) from exc

    def _validate(self, data: pd.DataFrame) -> None:
        """
        Validate loaded data.
        """
        try:
            if not isinstance(data, pd.DataFrame):
                raise DataValidationError("Data must be a csv file.")

            for index, record in enumerate(data):
                self._validate_record(record=record, record_index=index)

        except DataValidationError as exc:
            self.logger.error("Data validation error", exc=exc)
            raise

        except Exception as exc:
            self.logger.error("Unknown error during data validation", exc=exc)
            raise DataValidationError(
                "Unknown error during data validation", original_exception=exc
            ) from exc

    def _validate_record(
        self,
        record: dict[str, Any],
        record_index: int,
    ) -> None:
        """
        Validate a single record.
        """
        try:
            if not isinstance(record, dict):
                raise TypeError(f"Record {record_index} must be a dictionary.")

            if not self.REQUIRED_FIELDS:
                raise DataValidationError("No required fields defined for validation.")

            for field, expected_type in self.REQUIRED_FIELDS.items():
                if field not in record:
                    raise DataValidationError(
                        f"""Record {record_index} missing field '{field}'.
                        \n record: {record}"""
                    )

                if not isinstance(
                    record[field],
                    expected_type,
                ):
                    raise DataValidationError(
                        f"Record {record_index} field '{field}' \n record: {record}"
                        "\n"
                        f"must be {expected_type}."
                    )

            self._validate_business_rules(
                record=record,
                record_index=record_index,
            )

        except TypeError as exc:
            self.logger.error(
                f"Type error in record {record_index}\n record: {record}", exc=exc
            )
            raise DataValidationError(
                f"Type error in record {record_index}", original_exception=exc
            ) from exc

        except DataValidationError as exc:
            self.logger.error(
                f"Data validation error in record {record_index}\n record: {record}",
                exc=exc,
            )
            raise
        except Exception as exc:
            self.logger.error(
                f"Unknown error in record {record_index}\n record: {record}", exc=exc
            )
            raise DataValidationError(
                f"Unknown error in record {record_index}", original_exception=exc
            ) from exc

    def _validate_business_rules(
        self,
        record: dict[str, Any],
        record_index: int,
    ) -> None:
        """
        Additional validation rules.
        """
        if record["score"] < 0:
            self.logger.warning(
                f"""Record {record_index} has a negative score: {record["score"]}\n 
                record: {record}"""
            )
            raise DataValidationError(
                f"Record {record_index}: score cannot be negative."
            )

        if not record["name"].strip():
            self.logger.warning(
                f"""Record {record_index} has an empty name: {record["name"]}\n 
                record: {record}"""
            )
            raise DataValidationError(f"Record {record_index}: name cannot be empty.")
