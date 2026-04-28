"""PyQt6 GUI application for MagicSquare."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from magicsquare import MATRIX_SIZE
from magicsquare.boundary import solve, validate


class MainWindow(QMainWindow):
    """Main screen with 4x4 input grid and solve action."""

    def __init__(self) -> None:
        """Initialize UI components."""
        super().__init__()
        self.setWindowTitle("MagicSquare 4x4")
        self._inputs: list[list[QLineEdit]] = []
        self._result_label = QLabel("결과: [r1,c1,n1,r2,c2,n2]")
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the screen layout."""
        root = QWidget()
        layout = QVBoxLayout()

        grid_layout = QGridLayout()
        for row in range(MATRIX_SIZE):
            row_fields: list[QLineEdit] = []
            for col in range(MATRIX_SIZE):
                field = QLineEdit("0")
                field.setMaxLength(2)
                field.setFixedWidth(48)
                field.setPlaceholderText("0")
                grid_layout.addWidget(field, row, col)
                row_fields.append(field)
            self._inputs.append(row_fields)

        controls = QHBoxLayout()
        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve_clicked)
        controls.addWidget(solve_button)

        layout.addLayout(grid_layout)
        layout.addLayout(controls)
        layout.addWidget(self._result_label)
        root.setLayout(layout)
        self.setCentralWidget(root)

    def _read_matrix(self) -> list[list[int]]:
        """Read integer matrix values from the form."""
        matrix: list[list[int]] = []
        for row in self._inputs:
            values: list[int] = []
            for field in row:
                text = field.text().strip()
                if text == "":
                    values.append(0)
                else:
                    values.append(int(text))
            matrix.append(values)
        return matrix

    def _on_solve_clicked(self) -> None:
        """Run boundary validate->solve flow and show result or error."""
        try:
            matrix = self._read_matrix()
            validate(matrix)
            result = solve(matrix)
        except ValueError as exc:
            QMessageBox.critical(self, "입력 오류", str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "실행 오류", str(exc))
            return

        self._result_label.setText(f"결과: {result}")


def run() -> int:
    """Run the GUI event loop."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

