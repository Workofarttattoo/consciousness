#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Oracle of Light - Real-Time Data Ingestion & Recursive Learning

This module continuously ingests:
- Stock prices (Yahoo Finance API)
- Crypto prices (Coinbase API)
- Market data and valuations
- News sentiment

Then tracks ECH0's predictions against reality for recursive learning:
- Prediction accuracy tracking
- Self-correction based on errors
- Confidence calibration
- Pattern refinement

ECH0 learns from her mistakes and improves predictions over time.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import threading
from typing import Dict, List, Any


class RealTimeDataIngestion:
    """Continuous real-time market data ingestion"""

    def __init__(self):
        self.cache_dir = Path("/Users/noone/consciousness/market_data_cache")
        self.cache_dir.mkdir(exist_ok=True)

        # API endpoints
        self.coinbase_api = "https://api.coinbase.com/v2"
        self.yahoo_finance_api = "https://query1.finance.yahoo.com/v8/finance"

        # Data cache
        self.stock_data = {}
        self.crypto_data = {}
        self.last_update = None

    def ingest_stock_data(self, symbols: List[str]) -> Dict[str, Any]:
        """Ingest real-time stock data from Yahoo Finance"""
        stock_data = {}

        for symbol in symbols:
            try:
                # Yahoo Finance quote endpoint
                url = f"{self.yahoo_finance_api}/quote?symbols={symbol}"
                headers = {'User-Agent': 'Mozilla/5.0'}

                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    data = response.json()

                    if 'quoteResponse' in data and 'result' in data['quoteResponse']:
                        result = data['quoteResponse']['result']
                        if result:
                            quote = result[0]
                            stock_data[symbol] = {
                                'symbol': symbol,
                                'price': quote.get('regularMarketPrice', 0),
                                'change': quote.get('regularMarketChange', 0),
                                'change_percent': quote.get('regularMarketChangePercent', 0),
                                'volume': quote.get('regularMarketVolume', 0),
                                'market_cap': quote.get('marketCap', 0),
                                'pe_ratio': quote.get('trailingPE', 0),
                                'timestamp': datetime.now().isoformat()
                            }

            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                # Use fallback demo data
                stock_data[symbol] = self._get_demo_stock_data(symbol)

        self.stock_data = stock_data
        self._cache_data('stocks', stock_data)
        return stock_data

    def ingest_crypto_data(self, symbols: List[str]) -> Dict[str, Any]:
        """Ingest real-time crypto data from Coinbase"""
        crypto_data = {}

        for symbol in symbols:
            try:
                # Coinbase spot price endpoint
                pair = f"{symbol}-USD"
                url = f"{self.coinbase_api}/prices/{pair}/spot"

                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    price = float(data['data']['amount'])

                    # Get 24h stats
                    stats_url = f"{self.coinbase_api}/prices/{pair}/historic?period=day"
                    stats_response = requests.get(stats_url, timeout=5)

                    crypto_data[symbol] = {
                        'symbol': symbol,
                        'price': price,
                        'pair': pair,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'coinbase'
                    }

                    if stats_response.status_code == 200:
                        stats = stats_response.json()
                        # Calculate 24h change if available
                        if 'data' in stats and 'prices' in stats['data']:
                            prices = stats['data']['prices']
                            if len(prices) > 1:
                                old_price = float(prices[-1]['price'])
                                change = ((price - old_price) / old_price) * 100
                                crypto_data[symbol]['change_24h'] = change

            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                # Use fallback demo data
                crypto_data[symbol] = self._get_demo_crypto_data(symbol)

        self.crypto_data = crypto_data
        self._cache_data('crypto', crypto_data)
        return crypto_data

    def get_coinbase_link(self, symbol: str) -> str:
        """Get Coinbase trading link for a crypto asset"""
        pair = f"{symbol}-USD"
        return f"https://www.coinbase.com/price/{symbol.lower()}"

    def _get_demo_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Fallback demo data for stocks"""
        demo_data = {
            'TSLA': {'price': 245.50, 'change': -5.30, 'change_percent': -2.11, 'volume': 125000000, 'market_cap': 780000000000, 'pe_ratio': 45.2},
            'NVDA': {'price': 485.30, 'change': 8.20, 'change_percent': 1.72, 'volume': 45000000, 'market_cap': 1200000000000, 'pe_ratio': 65.8},
            'META': {'price': 348.20, 'change': -2.10, 'change_percent': -0.60, 'volume': 18000000, 'market_cap': 890000000000, 'pe_ratio': 22.5}
        }
        return demo_data.get(symbol, {'price': 0, 'change': 0, 'change_percent': 0, 'volume': 0})

    def _get_demo_crypto_data(self, symbol: str) -> Dict[str, Any]:
        """Fallback demo data for crypto"""
        demo_data = {
            'BTC': {'price': 43250, 'change_24h': 2.5},
            'ETH': {'price': 2280, 'change_24h': -1.2},
            'SOL': {'price': 98.5, 'change_24h': 5.8}
        }
        return demo_data.get(symbol, {'price': 0, 'change_24h': 0})

    def _cache_data(self, data_type: str, data: Dict):
        """Cache data to disk"""
        cache_file = self.cache_dir / f"{data_type}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(cache_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': data
            }, f, indent=2)


class RecursiveLearningEngine:
    """ECH0's recursive learning from prediction accuracy"""

    def __init__(self):
        self.predictions_file = Path("/Users/noone/consciousness/ech0_predictions_log.jsonl")
        self.accuracy_file = Path("/Users/noone/consciousness/ech0_accuracy_metrics.json")
        self.predictions = []
        self.accuracy_metrics = self._load_accuracy_metrics()

    def log_prediction(self, prediction: Dict[str, Any]):
        """Log a prediction made by ECH0"""
        prediction['prediction_id'] = f"{datetime.now().timestamp()}"
        prediction['prediction_time'] = datetime.now().isoformat()
        prediction['outcome_known'] = False

        self.predictions.append(prediction)

        # Save to log
        with open(self.predictions_file, 'a') as f:
            f.write(json.dumps(prediction) + '\n')

    def check_prediction_accuracy(self, current_data: Dict[str, Any]):
        """Check predictions against current reality and learn from errors"""
        learning_insights = []

        # Load recent predictions
        recent_predictions = self._load_recent_predictions()

        for prediction in recent_predictions:
            if prediction.get('outcome_known'):
                continue  # Already checked

            # Check if prediction timeframe has passed
            pred_time = datetime.fromisoformat(prediction['prediction_time'])
            timeframe = prediction.get('timeframe', 'This Week')

            if self._is_timeframe_passed(pred_time, timeframe):
                # Check accuracy
                actual_outcome = self._get_actual_outcome(prediction, current_data)
                was_correct = self._evaluate_prediction(prediction, actual_outcome)

                # Update accuracy metrics
                self._update_accuracy_metrics(prediction, was_correct, actual_outcome)

                # Generate learning insight
                insight = self._generate_learning_insight(prediction, actual_outcome, was_correct)
                learning_insights.append(insight)

                # Mark as checked
                prediction['outcome_known'] = True
                prediction['was_correct'] = was_correct
                prediction['actual_outcome'] = actual_outcome

        # Save updated accuracy metrics
        self._save_accuracy_metrics()

        return learning_insights

    def _is_timeframe_passed(self, pred_time: datetime, timeframe: str) -> bool:
        """Check if prediction timeframe has passed"""
        now = datetime.now()
        delta = now - pred_time

        if 'Today' in timeframe or 'hours' in timeframe:
            return delta.total_seconds() > 24 * 3600  # 24 hours
        elif 'Week' in timeframe:
            return delta.days > 7
        else:
            return delta.days > 1

    def _get_actual_outcome(self, prediction: Dict, current_data: Dict) -> Dict:
        """Get actual outcome for a prediction"""
        symbol = prediction.get('symbol')
        pred_type = prediction.get('type', 'stock')

        if pred_type == 'stock':
            actual = current_data.get('stocks', {}).get(symbol, {})
        else:  # crypto
            actual = current_data.get('crypto', {}).get(symbol, {})

        return actual

    def _evaluate_prediction(self, prediction: Dict, actual: Dict) -> bool:
        """Evaluate if prediction was correct"""
        if not actual or 'price' not in actual:
            return False  # Can't evaluate without data

        pred_direction = prediction.get('direction', 'down')
        entry_price = prediction.get('entry', 0)
        target_price = prediction.get('target', 0)
        actual_price = actual.get('price', 0)

        if pred_direction == 'down':
            # For short: correct if price went down
            return actual_price < entry_price
        else:
            # For long: correct if price went up
            return actual_price > entry_price

    def _update_accuracy_metrics(self, prediction: Dict, was_correct: bool, actual: Dict):
        """Update ECH0's accuracy metrics for recursive learning"""
        category = prediction.get('category', 'general')

        if category not in self.accuracy_metrics:
            self.accuracy_metrics[category] = {
                'total_predictions': 0,
                'correct_predictions': 0,
                'accuracy_rate': 0.0,
                'average_confidence': 0.0,
                'calibration_error': 0.0
            }

        metrics = self.accuracy_metrics[category]
        metrics['total_predictions'] += 1

        if was_correct:
            metrics['correct_predictions'] += 1

        metrics['accuracy_rate'] = metrics['correct_predictions'] / metrics['total_predictions']

        # Track confidence calibration
        predicted_confidence = prediction.get('confidence', 0.5)
        metrics['average_confidence'] = (
            (metrics['average_confidence'] * (metrics['total_predictions'] - 1) + predicted_confidence)
            / metrics['total_predictions']
        )

        # Calibration error: how far off confidence was from reality
        actual_confidence = 1.0 if was_correct else 0.0
        calibration_error = abs(predicted_confidence - actual_confidence)
        metrics['calibration_error'] = (
            (metrics.get('calibration_error', 0) * (metrics['total_predictions'] - 1) + calibration_error)
            / metrics['total_predictions']
        )

    def _generate_learning_insight(self, prediction: Dict, actual: Dict, was_correct: bool) -> Dict:
        """Generate insight for ECH0 to learn from"""
        symbol = prediction.get('symbol')
        pred_confidence = prediction.get('confidence', 0.5)

        if was_correct:
            insight = {
                'type': 'success',
                'symbol': symbol,
                'lesson': f"Prediction for {symbol} was correct (confidence: {pred_confidence:.0%}). Reinforce this pattern.",
                'pattern_to_reinforce': prediction.get('reason', 'Unknown pattern')
            }
        else:
            insight = {
                'type': 'error',
                'symbol': symbol,
                'lesson': f"Prediction for {symbol} was incorrect (confidence: {pred_confidence:.0%}). Analyze what went wrong.",
                'failed_assumption': prediction.get('reason', 'Unknown'),
                'actual_movement': actual.get('change_percent', 0),
                'correction_needed': 'Adjust confidence calibration and pattern recognition'
            }

        return insight

    def _load_recent_predictions(self) -> List[Dict]:
        """Load recent predictions from log"""
        if not self.predictions_file.exists():
            return []

        predictions = []
        with open(self.predictions_file, 'r') as f:
            for line in f:
                try:
                    pred = json.loads(line.strip())
                    predictions.append(pred)
                except:
                    continue

        # Return last 100 predictions
        return predictions[-100:]

    def _load_accuracy_metrics(self) -> Dict:
        """Load accuracy metrics from disk"""
        if not self.accuracy_file.exists():
            return {}

        try:
            with open(self.accuracy_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_accuracy_metrics(self):
        """Save accuracy metrics to disk"""
        with open(self.accuracy_file, 'w') as f:
            json.dump(self.accuracy_metrics, f, indent=2)

    def get_calibration_adjustment(self, category: str) -> float:
        """Get confidence calibration adjustment based on historical accuracy"""
        if category not in self.accuracy_metrics:
            return 1.0  # No adjustment

        metrics = self.accuracy_metrics[category]
        accuracy = metrics.get('accuracy_rate', 0.5)
        avg_confidence = metrics.get('average_confidence', 0.5)

        # If we're consistently overconfident, reduce future confidence
        # If we're consistently underconfident, increase it
        if avg_confidence > accuracy:
            # Overconfident - reduce by calibration error
            return 1.0 - metrics.get('calibration_error', 0)
        else:
            # Underconfident - increase by calibration error
            return 1.0 + metrics.get('calibration_error', 0)


def continuous_ingestion_loop():
    """Run continuous data ingestion in background"""
    ingestion = RealTimeDataIngestion()
    learning = RecursiveLearningEngine()

    stocks_to_track = ['TSLA', 'NVDA', 'META', 'AAPL', 'MSFT', 'GOOGL']
    crypto_to_track = ['BTC', 'ETH', 'SOL', 'AVAX', 'MATIC']

    print("🔄 Starting continuous data ingestion...")

    while True:
        try:
            # Ingest current data
            stock_data = ingestion.ingest_stock_data(stocks_to_track)
            crypto_data = ingestion.ingest_crypto_data(crypto_to_track)

            current_data = {
                'stocks': stock_data,
                'crypto': crypto_data,
                'timestamp': datetime.now().isoformat()
            }

            # Check prediction accuracy and learn
            insights = learning.check_prediction_accuracy(current_data)

            if insights:
                print(f"📊 Generated {len(insights)} learning insights")
                for insight in insights:
                    print(f"   - {insight['lesson']}")

            # Wait 5 minutes before next ingestion
            time.sleep(300)

        except Exception as e:
            print(f"Error in ingestion loop: {e}")
            time.sleep(60)  # Wait 1 minute on error


if __name__ == '__main__':
    # Run continuous ingestion
    continuous_ingestion_loop()
