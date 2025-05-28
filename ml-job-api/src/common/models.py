from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


#


class BasePostgresModel(DeclarativeBase):
    """
    Base class for all PostgreSQL ORM models, providing:
      - A global `metadata` object with a consistent naming convention for
        primary keys, indexes, foreign keys, unique constraints, and checks.
      - A customizable `__repr__` that includes a selection of columns.

    Attributes:
        repr_columns (tuple[str, ...]):
            Column names to always include in the repr output, even beyond
            the default `repr_columns_number`.
        repr_columns_number (int):
            Number of leading columns to include in the repr output if
            `repr_columns` is empty.
    """

    # Apply structured naming conventions for DB constraints and indexes
    metadata = MetaData(
        naming_convention={
            "all_column_names": lambda constraint, table: "_".join(
                [column.name for column in constraint.columns.values()]
            ),
            "pk": "pk__%(table_name)s",
            "ix": "ix__%(table_name)s__%(all_column_names)s",
            "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
            "uq": "uq__%(table_name)s__%(all_column_names)s",
            "ck": "ck__%(table_name)s__%(constraint_name)s",
        },
    )

    repr_columns = tuple()
    repr_columns_number = 3

    def __repr__(self) -> str:
        """
        Generate a concise representation of the ORM object.

        It includes either:
          - All columns named in `repr_columns`, or
          - The first `repr_columns_number` columns in table order.

        Returns:
            str: A string like "<ModelName(col1=val1, col2=val2, ...)>".
        """

        columns = []

        for idx, column in enumerate(self.__table__.columns.keys()):
            if column in self.repr_columns or idx < self.repr_columns_number:
                columns.append(f"{column}={getattr(self, column)!r}")

        return f"<{self.__class__.__name__}({', '.join(columns)})>"
