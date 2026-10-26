# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Oct 25, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: the chart selected in the list, the Show button
Processing: reading of the totals calculated by MySQL with GROUP BY through the
database_manager module (sales by month, sales by category, stock of each item, restock
cost by supplier), drawing of the chart with matplotlib on a canvas inside the form
Outputs: the chart displayed with its navigation toolbar (zoom, move, save as an image),
a summary message under the chart
"""
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QComboBox,
                             QGridLayout, QVBoxLayout)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import database_manager
from report_form import DEFAULT_STOCK_LEVEL

CHART_SALES_MONTH = 'Sales by month'
CHART_SALES_CATEGORY = 'Sales by category'
CHART_STOCK = 'Stock of each item'
CHART_RESTOCK_COST = 'Restock cost by supplier'

# the rose of the application and darker or lighter tones of it
COLOR_ROSE = '#A23E5C'
COLOR_LOW = '#B22222'
COLOR_LINE = '#555555'
PIE_COLORS = ['#A23E5C', '#7A2D47', '#C76B87', '#8E6C78', '#5E1F33', '#B5546F']

MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov',
               'Dec']


class MptCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)  # 1 row, 1 column, chart 1
        super().__init__(fig)


class AnalyticsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, analytics')

        self.label_title = QLabel('Analytics')
        self.label_title.setObjectName('title')
        self.label_chart = QLabel('Chart:')
        self.label_message = QLabel('')

        self.combo_chart = QComboBox()
        self.combo_chart.addItem(CHART_SALES_MONTH)
        self.combo_chart.addItem(CHART_SALES_CATEGORY)
        self.combo_chart.addItem(CHART_STOCK)
        self.combo_chart.addItem(CHART_RESTOCK_COST)

        self.button_show = QPushButton('Show')

        # creating the figure canvas object, which defines the set of axes
        self.canvas = MptCanvas(self, width=8, height=4.5, dpi=100)
        # navigation bar of the chart: zoom, move, save as an image
        self.toolbar = NavigationToolbar(self.canvas)

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.button_show.clicked.connect(self.showChart)
        self.combo_chart.currentIndexChanged.connect(self.showChart)

        self.showChart()

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(3, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 4)
        grid.addWidget(self.label_chart, 1, 0)
        grid.addWidget(self.combo_chart, 1, 1)
        grid.addWidget(self.button_show, 1, 2)

        chart_layout = QVBoxLayout()
        chart_layout.addWidget(self.toolbar)
        chart_layout.addWidget(self.canvas)
        grid.addLayout(chart_layout, 2, 0, 1, 4)
        grid.setRowStretch(2, 1)

        grid.addWidget(self.label_message, 3, 0, 1, 4)

        self.setLayout(grid)

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    # the figure is cleared and its axes created again, because the pie chart leaves its
    # round proportions on the axes; then the selected chart is drawn and the canvas repainted
    def showChart(self):
        selected_chart = self.combo_chart.currentText()
        self.canvas.figure.clear()
        self.canvas.axes = self.canvas.figure.add_subplot(111)

        if selected_chart == CHART_SALES_MONTH:
            self.drawSalesByMonth()
        elif selected_chart == CHART_SALES_CATEGORY:
            self.drawSalesByCategory()
        elif selected_chart == CHART_STOCK:
            self.drawStockLevels()
        elif selected_chart == CHART_RESTOCK_COST:
            self.drawRestockCost()

        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def drawSalesByMonth(self):
        month_list = []
        sales_list = []
        total_orders = 0
        total_sales = 0.0
        for row in database_manager.load_sales_by_month():
            month_list.append(MONTH_NAMES[row[1] - 1] + ' ' + str(row[0]))
            sales_list.append(float(row[3]))
            total_orders = total_orders + row[2]
            total_sales = total_sales + float(row[3])

        if len(month_list) == 0:
            self.showMessage('No paid order yet: the chart is empty.', True)
            return

        bars = self.canvas.axes.bar(month_list, sales_list, color=COLOR_ROSE)
        self.canvas.axes.bar_label(bars, fmt='%.2f $')
        self.canvas.axes.set_ylim(0, max(sales_list) * 1.15)
        self.canvas.axes.set_title('Sales by month, paid orders')
        self.canvas.axes.set_ylabel('Subtotal before fees and taxes ($)')

        self.showMessage(str(total_orders) + ' paid order(s) in ' + str(len(month_list))
                         + ' month(s), subtotal ' + format(total_sales, '.2f') + ' $.', False)

    def drawSalesByCategory(self):
        category_list = []
        sales_list = []
        total_sales = 0.0
        for row in database_manager.load_sales_by_category():
            category_list.append(row[0])
            sales_list.append(float(row[1]))
            total_sales = total_sales + float(row[1])

        if len(category_list) == 0:
            self.showMessage('No paid order yet: the chart is empty.', True)
            return

        wedges, labels, percents = self.canvas.axes.pie(sales_list, labels=category_list,
                                                        colors=PIE_COLORS, autopct='%1.1f%%',
                                                        startangle=90)
        for percent in percents:
            percent.set_color('white')
        self.canvas.axes.set_title('Sales by category, paid orders')

        # the rows come from MySQL sorted by sales, the first category is the best seller
        self.showMessage(category_list[0] + ' sells the most: ' + format(sales_list[0], '.2f')
                         + ' $ out of ' + format(total_sales, '.2f') + ' $.', False)

    def drawStockLevels(self):
        item_list = []
        stock_list = []
        color_list = []
        total_low = 0
        total_out = 0
        for row in database_manager.load_stock_levels():
            item_list.append(row[0] + ' ' + row[1])
            stock_list.append(row[2])
            if row[2] <= DEFAULT_STOCK_LEVEL:
                color_list.append(COLOR_LOW)
                total_low = total_low + 1
            else:
                color_list.append(COLOR_ROSE)
            if row[2] == 0:
                total_out = total_out + 1

        if len(item_list) == 0:
            self.showMessage('The catalog is empty.', True)
            return

        bars = self.canvas.axes.barh(item_list, stock_list, color=color_list)
        self.canvas.axes.bar_label(bars)
        self.canvas.axes.axvline(DEFAULT_STOCK_LEVEL, color=COLOR_LINE, linestyle='--',
                                 label='Low stock level: ' + str(DEFAULT_STOCK_LEVEL))
        self.canvas.axes.legend()
        self.canvas.axes.set_title('Stock of each item, low stock in red')
        self.canvas.axes.set_xlabel('Units in stock')

        self.showMessage(str(total_low) + ' item(s) at ' + str(DEFAULT_STOCK_LEVEL)
                         + ' or less, ' + str(total_out) + ' out of stock.', False)

    def drawRestockCost(self):
        supplier_list = []
        cost_list = []
        total_restocks = 0
        total_cost = 0.0
        for row in database_manager.load_restock_cost_by_supplier():
            supplier_list.append(row[0])
            cost_list.append(float(row[2]))
            total_restocks = total_restocks + row[1]
            total_cost = total_cost + float(row[2])

        if len(supplier_list) == 0:
            self.showMessage('No restock yet: the chart is empty.', True)
            return

        bars = self.canvas.axes.barh(supplier_list, cost_list, color=COLOR_ROSE)
        self.canvas.axes.bar_label(bars, fmt='%.2f $')
        self.canvas.axes.set_xlim(0, max(cost_list) * 1.2)
        self.canvas.axes.set_title('Restock cost by supplier')
        self.canvas.axes.set_xlabel('Cost of the restocks ($)')

        self.showMessage(str(total_restocks) + ' restock(s), total cost '
                         + format(total_cost, '.2f') + ' $.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the window of the analytics form
    window = AnalyticsForm()
    window.resize(1000, 620)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
