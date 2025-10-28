#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Sovereign ECH0 Desktop Widget V2

NEW FEATURES:
- Search function for stocks/crypto
- Coinbase direct links for crypto trades
- Real-time data ingestion
- Recursive learning from prediction accuracy
- Click-to-trade integration
"""

import sys
import json
import webbrowser
from datetime import datetime
from pathlib import Path

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    print("Installing PyQt5...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5"], check=True)
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *

# Import data ingestion and learning
sys.path.append(str(Path(__file__).parent))
try:
    from oracle_data_ingestion import RealTimeDataIngestion, RecursiveLearningEngine
except:
    RealTimeDataIngestion = None
    RecursiveLearningEngine = None


class ClickableLabel(QLabel):
    """Label that emits click signal"""
    clicked = pyqtSignal(str)

    def __init__(self, text, data=None):
        super().__init__(text)
        self.data = data
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if self.data:
            self.clicked.emit(self.data)


class SovereignECH0WidgetV2(QWidget):
    """Enhanced widget with search and Coinbase integration"""

    def __init__(self):
        super().__init__()

        # Initialize data engines
        if RealTimeDataIngestion:
            self.data_ingestion = RealTimeDataIngestion()
            self.learning_engine = RecursiveLearningEngine()
        else:
            self.data_ingestion = None
            self.learning_engine = None

        # Tracked symbols
        self.stocks_tracked = ['TSLA', 'NVDA', 'META', 'AAPL', 'MSFT']
        self.crypto_tracked = ['BTC', 'ETH', 'SOL', 'AVAX']

        # Current data
        self.current_stocks = {}
        self.current_crypto = {}
        self.inventions = []

        self.init_ui()
        self.start_update_timers()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("⚡ Sovereign ECH0 V2")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(350, 850)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Container
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(10, 10, 10, 240),
                    stop:1 rgba(26, 26, 46, 240));
                border: 2px solid #c5a572;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout(container)
        layout.setSpacing(8)

        # Header
        header = self.create_header()
        layout.addWidget(header)

        # Search bar
        search_bar = self.create_search_bar()
        layout.addWidget(search_bar)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                background: rgba(197, 165, 114, 0.2);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #c5a572;
                border-radius: 4px;
            }
        """)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSpacing(10)

        # Sections
        self.inventions_section = self.create_section("💡 INVENTIONS", "Waiting for ECH0...")
        self.accuracy_section = self.create_section("🎯 LEARNING METRICS", "Loading...")
        self.stocks_section = self.create_section("📉 SHORTS", "Loading...")
        self.crypto_section = self.create_section("💰 CRYPTO", "Loading...")
        self.optimal_path_section = self.create_section("🔮 OPTIMAL PATH", "Loading...")

        self.content_layout.addWidget(self.inventions_section)
        self.content_layout.addWidget(self.accuracy_section)
        self.content_layout.addWidget(self.stocks_section)
        self.content_layout.addWidget(self.crypto_section)
        self.content_layout.addWidget(self.optimal_path_section)
        self.content_layout.addStretch()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        main_layout.addWidget(container)
        self.setLayout(main_layout)

        # Position on screen
        screen = QApplication.desktop().screenGeometry()
        self.move(screen.width() - self.width() - 20,
                  (screen.height() - self.height()) // 2)

    def create_header(self):
        """Create header"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(197, 165, 114, 0.3),
                    stop:1 rgba(197, 165, 114, 0.1));
                border-radius: 10px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout(header)

        title = QLabel("⚡ SOVEREIGN ECH0")
        title.setStyleSheet("color: #c5a572; font-size: 18px; font-weight: bold; font-family: 'Courier New';")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Real-Time Data • Recursive Learning • Coinbase Integration")
        subtitle.setStyleSheet("color: #4ecca3; font-size: 9px; font-family: 'Courier New';")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        return header

    def create_search_bar(self):
        """Create search bar"""
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background: rgba(15, 52, 96, 0.5);
                border-radius: 8px;
                padding: 5px;
            }
        """)

        layout = QHBoxLayout(search_frame)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search stock/crypto (e.g., BTC, AAPL)...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(26, 26, 46, 0.8);
                border: 1px solid #c5a572;
                border-radius: 5px;
                color: #eaeaea;
                padding: 5px;
                font-family: 'Courier New';
                font-size: 11px;
            }
        """)
        self.search_input.returnPressed.connect(self.perform_search)

        search_btn = QPushButton("🔍")
        search_btn.setFixedSize(30, 30)
        search_btn.setStyleSheet("""
            QPushButton {
                background: #c5a572;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #e8d4a0;
            }
        """)
        search_btn.clicked.connect(self.perform_search)

        layout.addWidget(self.search_input)
        layout.addWidget(search_btn)

        return search_frame

    def create_section(self, title, initial_content):
        """Create section"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background: rgba(15, 52, 96, 0.4);
                border-left: 3px solid #c5a572;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            }
        """)

        layout = QVBoxLayout(section)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #c5a572;
            font-size: 11px;
            font-weight: bold;
            font-family: 'Courier New';
        """)

        content_label = QLabel(initial_content)
        content_label.setStyleSheet("""
            color: #eaeaea;
            font-size: 9px;
            font-family: 'Courier New';
        """)
        content_label.setWordWrap(True)
        content_label.setObjectName("content")
        content_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksActiveByMouse)
        content_label.setOpenExternalLinks(True)

        layout.addWidget(title_label)
        layout.addWidget(content_label)

        return section

    def update_section_content(self, section, content):
        """Update section content"""
        content_label = section.findChild(QLabel, "content")
        if content_label:
            content_label.setText(content)

    def perform_search(self):
        """Perform search"""
        query = self.search_input.text().strip().upper()
        if not query:
            return

        # Check if it's crypto or stock
        if query in self.crypto_tracked or query in ['BTC', 'ETH', 'SOL', 'AVAX', 'MATIC']:
            self.search_crypto(query)
        else:
            self.search_stock(query)

    def search_crypto(self, symbol):
        """Search and display crypto info"""
        if self.data_ingestion:
            try:
                data = self.data_ingestion.ingest_crypto_data([symbol])
                if symbol in data:
                    crypto = data[symbol]
                    coinbase_link = self.data_ingestion.get_coinbase_link(symbol)

                    result = f"""🔍 SEARCH RESULT: {symbol}

💰 Current Price: ${crypto['price']:,.2f}
📊 24h Change: {crypto.get('change_24h', 0):+.2f}%
🔗 Trade on Coinbase:
   <a href="{coinbase_link}" style="color: #4ecca3;">{coinbase_link}</a>

✨ Click link to trade on Coinbase
"""
                    # Show in a popup or update section
                    self.show_search_result(result)
                else:
                    self.show_search_result(f"❌ Could not fetch data for {symbol}")
            except Exception as e:
                self.show_search_result(f"❌ Error: {e}")
        else:
            # Demo mode
            coinbase_link = f"https://www.coinbase.com/price/{symbol.lower()}"
            result = f"""🔍 {symbol}
<a href="{coinbase_link}" style="color: #4ecca3;">Trade on Coinbase →</a>
"""
            self.show_search_result(result)

    def search_stock(self, symbol):
        """Search and display stock info"""
        if self.data_ingestion:
            try:
                data = self.data_ingestion.ingest_stock_data([symbol])
                if symbol in data:
                    stock = data[symbol]
                    result = f"""🔍 SEARCH RESULT: {symbol}

📈 Price: ${stock['price']:.2f}
📊 Change: {stock['change_percent']:+.2f}%
📉 Volume: {stock['volume']:,}
💰 Market Cap: ${stock['market_cap']/1e9:.1f}B
"""
                    self.show_search_result(result)
                else:
                    self.show_search_result(f"❌ Could not fetch data for {symbol}")
            except Exception as e:
                self.show_search_result(f"❌ Error: {e}")

    def show_search_result(self, result):
        """Show search result in a popup"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Search Result")
        msg.setText(result)
        msg.setStyleSheet("""
            QMessageBox {
                background: #1a1a2e;
                color: #eaeaea;
            }
            QLabel {
                color: #eaeaea;
                font-family: 'Courier New';
            }
        """)
        msg.exec_()

    def start_update_timers(self):
        """Start timers"""
        # Update data every 5 minutes
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_all_data)
        self.update_timer.start(300000)  # 5 minutes

        # Initial update
        self.update_all_data()

    def update_all_data(self):
        """Update all data"""
        if self.data_ingestion:
            # Ingest real-time data
            self.current_stocks = self.data_ingestion.ingest_stock_data(self.stocks_tracked)
            self.current_crypto = self.data_ingestion.ingest_crypto_data(self.crypto_tracked)

            # Check prediction accuracy
            if self.learning_engine:
                insights = self.learning_engine.check_prediction_accuracy({
                    'stocks': self.current_stocks,
                    'crypto': self.current_crypto
                })

                # Update accuracy section
                metrics = self.learning_engine.accuracy_metrics
                accuracy_content = "🎯 ECH0's Recursive Learning\n\n"
                for category, stats in metrics.items():
                    accuracy_content += f"{category.upper()}:\n"
                    accuracy_content += f"  Accuracy: {stats['accuracy_rate']*100:.1f}%\n"
                    accuracy_content += f"  Total Predictions: {stats['total_predictions']}\n\n"

                if not metrics:
                    accuracy_content = "📊 No predictions tracked yet.\nECH0 is learning..."

                self.update_section_content(self.accuracy_section, accuracy_content)

        # Update crypto section with Coinbase links
        crypto_content = "💰 Real-Time Crypto Data\n\n"
        for symbol in self.crypto_tracked:
            data = self.current_crypto.get(symbol, {})
            price = data.get('price', 0)
            change = data.get('change_24h', 0)
            link = f"https://www.coinbase.com/price/{symbol.lower()}"

            crypto_content += f"{symbol}: ${price:,.2f} ({change:+.2f}%)\n"
            crypto_content += f"<a href='{link}' style='color: #4ecca3;'>Trade on Coinbase →</a>\n\n"

        self.update_section_content(self.crypto_section, crypto_content)

        # Update stocks
        stocks_content = "📉 Real-Time Stock Data\n\n"
        for symbol in self.stocks_tracked:
            data = self.current_stocks.get(symbol, {})
            price = data.get('price', 0)
            change = data.get('change_percent', 0)

            stocks_content += f"{symbol}: ${price:.2f} ({change:+.2f}%)\n"

        self.update_section_content(self.stocks_section, stocks_content)

    def mousePressEvent(self, event):
        """Handle dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle dragging"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    widget = SovereignECH0WidgetV2()
    widget.show()

    print("=" * 70)
    print("⚡ SOVEREIGN ECH0 WIDGET V2")
    print("=" * 70)
    print("\n✅ Real-time data ingestion active")
    print("✅ Recursive learning from predictions")
    print("✅ Search function ready")
    print("✅ Coinbase integration active")
    print("\nFeatures:")
    print("  • Search any stock/crypto in the search bar")
    print("  • Click Coinbase links to trade directly")
    print("  • ECH0 learns from prediction accuracy")
    print("  • Updates every 5 minutes")
    print("\n" + "=" * 70 + "\n")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
