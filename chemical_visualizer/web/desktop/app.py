import sys

import matplotlib
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
	QApplication,
	QFileDialog,
	QFormLayout,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QListWidget,
	QListWidgetItem,
	QMainWindow,
	QMessageBox,
	QPushButton,
	QTableWidget,
	QTableWidgetItem,
	QVBoxLayout,
	QWidget,
)
from requests.auth import HTTPBasicAuth


matplotlib.use("Qt5Agg")

API_URL = "http://127.0.0.1:8000/api"


class ChartWidget(FigureCanvas):
	def __init__(self, parent=None):
		self.figure = Figure(figsize=(4, 3))
		self.axes = self.figure.add_subplot(111)
		super().__init__(self.figure)
		self.setParent(parent)

	def plot_type_distribution(self, distribution):
		self.axes.clear()
		labels = list(distribution.keys())
		values = list(distribution.values())
		self.axes.bar(labels, values, color="#4c6ef5")
		self.axes.set_title("Type Distribution")
		self.axes.set_ylabel("Count")
		self.axes.tick_params(axis="x", rotation=45)
		self.figure.tight_layout()
		self.draw()


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
		self.resize(1200, 700)

		self.username_input = QLineEdit("admin")
		self.password_input = QLineEdit("admin123")
		self.password_input.setEchoMode(QLineEdit.Password)

		self.status_label = QLabel("Ready")
		self.summary_label = QLabel("No dataset loaded.")
		self.summary_label.setWordWrap(True)
		self.stats_label = QLabel("")
		self.stats_label.setWordWrap(True)
		self.history_list = QListWidget()
		self.table = QTableWidget(0, 0)

		self.chart = ChartWidget()

		upload_button = QPushButton("Upload CSV")
		upload_button.clicked.connect(self.upload_csv)

		refresh_button = QPushButton("Refresh History")
		refresh_button.clicked.connect(self.fetch_history)

		report_button = QPushButton("Download PDF Report")
		report_button.clicked.connect(self.download_report)

		auth_layout = QFormLayout()
		auth_layout.addRow("Username", self.username_input)
		auth_layout.addRow("Password", self.password_input)

		left_layout = QVBoxLayout()
		left_layout.addLayout(auth_layout)
		left_layout.addWidget(upload_button)
		left_layout.addWidget(refresh_button)
		left_layout.addWidget(report_button)
		left_layout.addWidget(QLabel("Recent Datasets"))
		left_layout.addWidget(self.history_list)
		left_layout.addWidget(self.status_label)

		right_layout = QVBoxLayout()
		right_layout.addWidget(self.summary_label)
		right_layout.addWidget(self.stats_label)
		right_layout.addWidget(self.chart)
		right_layout.addWidget(self.table)

		main_layout = QHBoxLayout()
		main_layout.addLayout(left_layout, 1)
		main_layout.addLayout(right_layout, 3)

		container = QWidget()
		container.setLayout(main_layout)
		self.setCentralWidget(container)

		self.history_list.itemClicked.connect(self.load_from_history)

		self.current_dataset_id = None
		self.fetch_history()
		self.fetch_latest()

	def auth(self):
		return HTTPBasicAuth(self.username_input.text(), self.password_input.text())

	def set_status(self, message):
		self.status_label.setText(message)

	def fetch_history(self):
		try:
			response = requests.get(f"{API_URL}/history/", auth=self.auth(), timeout=10)
			response.raise_for_status()
			self.history_list.clear()
			for item in response.json():
				list_item = QListWidgetItem(f"{item['name']} ({item['uploaded_at']})")
				list_item.setData(Qt.UserRole, item["id"])
				self.history_list.addItem(list_item)
			self.set_status("History loaded.")
		except requests.RequestException:
			self.set_status("Failed to load history.")

	def fetch_latest(self):
		try:
			response = requests.get(f"{API_URL}/datasets/latest/", auth=self.auth(), timeout=10)
			if response.status_code == 404:
				return
			response.raise_for_status()
			self.render_dataset(response.json())
		except requests.RequestException:
			pass

	def upload_csv(self):
		file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
		if not file_path:
			return

		try:
			with open(file_path, "rb") as file:
				response = requests.post(
					f"{API_URL}/upload/",
					files={"file": file},
					auth=self.auth(),
					timeout=30,
				)
			response.raise_for_status()
			self.render_dataset(response.json())
			self.fetch_history()
			self.set_status("Upload successful.")
		except requests.RequestException as exc:
			self.set_status("Upload failed.")
			QMessageBox.warning(self, "Upload Failed", str(exc))

	def load_from_history(self, item):
		dataset_id = item.data(Qt.UserRole)
		try:
			response = requests.get(
				f"{API_URL}/datasets/{dataset_id}/", auth=self.auth(), timeout=10
			)
			response.raise_for_status()
			self.render_dataset(response.json())
			self.set_status("Dataset loaded.")
		except requests.RequestException:
			self.set_status("Failed to load dataset.")

	def download_report(self):
		if not self.current_dataset_id:
			return
		save_path, _ = QFileDialog.getSaveFileName(
			self, "Save PDF Report", f"dataset-report-{self.current_dataset_id}.pdf", "PDF Files (*.pdf)"
		)
		if not save_path:
			return
		try:
			response = requests.get(
				f"{API_URL}/report/{self.current_dataset_id}/", auth=self.auth(), timeout=20
			)
			response.raise_for_status()
			with open(save_path, "wb") as file:
				file.write(response.content)
			self.set_status("Report saved.")
		except requests.RequestException:
			self.set_status("Failed to download report.")

	def render_dataset(self, dataset):
		self.current_dataset_id = dataset.get("id")
		summary = dataset.get("summary", {})
		self.summary_label.setText(
			" | ".join(
				[
					f"Total: {summary.get('total', 0)}",
					f"Total Uploaded: {summary.get('total_raw', summary.get('total', 0))}",
					f"Invalid Rows: {summary.get('invalid_rows', 0)}",
				]
			)
		)
		self.stats_label.setText(
			" | ".join(
				[
					f"Avg Flowrate: {summary.get('avg_flow', 0):.2f}",
					f"Avg Pressure: {summary.get('avg_pressure', 0):.2f}",
					f"Avg Temp: {summary.get('avg_temp', 0):.2f}",
					f"Flow Min/Max: {summary.get('min_flow', 0):.2f}/{summary.get('max_flow', 0):.2f}",
					f"Pressure Min/Max: {summary.get('min_pressure', 0):.2f}/{summary.get('max_pressure', 0):.2f}",
					f"Temp Min/Max: {summary.get('min_temp', 0):.2f}/{summary.get('max_temp', 0):.2f}",
				]
			)
		)

		distribution = summary.get("type_dist", {})
		self.chart.plot_type_distribution(distribution)

		data = dataset.get("data", [])
		columns = dataset.get("columns", [])
		self.table.setColumnCount(len(columns))
		self.table.setRowCount(len(data))
		self.table.setHorizontalHeaderLabels(columns)

		for row_index, row in enumerate(data):
			for col_index, col_name in enumerate(columns):
				value = row.get(col_name, "")
				item = QTableWidgetItem(str(value))
				self.table.setItem(row_index, col_index, item)


def main():
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
