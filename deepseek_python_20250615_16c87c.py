import yfinance as yf
from indicators import rsi, macd, ema, bollinger_bands
from patterns import detect_patterns
import pandas as pd

def generate_analysis(symbol: str, timeframe: str = "1h"):
    tf_map = {
        "5m": "5m", "15m": "15m", "30m": "30m", 
        "1h": "60m", "4h": "60m", "1d": "1d", "1w": "1wk"
    }
    tf = tf_map.get(timeframe, "60m")
    
    try:
        if symbol in ['XAUUSD', 'GOLD']:
            symbol_str = 'GC=F'
        elif symbol in ['USOIL', 'OIL']:
            symbol_str = 'CL=F'
        elif any(c in symbol for c in ['USD', 'EUR', 'GBP', 'JPY']):
            symbol_str = f"{symbol}=X" if "=X" not in symbol else symbol
        else:
            symbol_str = symbol

        df = yf.download(tickers=symbol_str, interval=tf, period="7d", progress=False)
        if df.empty:
            return f"❌ لا توجد بيانات لـ {symbol} ({symbol_str})"
            
        df = df.dropna()
        
        df["RSI"] = rsi(df["Close"])
        df["MACD"], df["Signal"] = macd(df["Close"])
        df["EMA20"] = ema(df["Close"], 20)
        df["EMA50"] = ema(df["Close"], 50)
        df["UpperBB"], df["LowerBB"] = bollinger_bands(df["Close"])
        
        pattern = detect_patterns(df)
        
        signals = []
        current_close = df["Close"].iloc[-1]
        
        rsi_val = df["RSI"].iloc[-1]
        if rsi_val < 30:
            signals.append("📉 RSI < 30 (تشبع بيعي)")
        elif rsi_val > 70:
            signals.append("📈 RSI > 70 (تشبع شرائي)")
        
        if df["MACD"].iloc[-1] > df["Signal"].iloc[-1]:
            signals.append("📈 MACD فوق خط الإشارة")
        else:
            signals.append("📉 MACD تحت خط الإشارة")
            
        if df["EMA20"].iloc[-1] > df["EMA50"].iloc[-1]:
            signals.append("📊 اتجاه صاعد (EMA20 > EMA50)")
        else:
            signals.append("📊 اتجاه هابط (EMA20 < EMA50)")
            
        if current_close < df["LowerBB"].iloc[-1]:
            signals.append("⚠️ السعر تحت النطاق السفلي (تشبع بيعي)")
        elif current_close > df["UpperBB"].iloc[-1]:
            signals.append("⚠️ السعر فوق النطاق العلوي (تشبع شرائي)")
        
        report = f"""
📊 **تحليل فني لـ {symbol} ({timeframe})**
────────────────────────
💵 السعر الحالي: {current_close:.4f}
📈 أعلى سعر: {df['High'].max():.4f}
📉 أدنى سعر: {df['Low'].min():.4f}

📌 **الإشارات الفنية:**
{chr(10).join(signals)}

🔍 **النمط الفني:** {pattern if pattern else "لا يوجد نمط واضح"}

📅 البيانات من: {df.index[0].strftime('%Y-%m-%d')} إلى {df.index[-1].strftime('%Y-%m-%d')}
"""
        return report
        
    except Exception as e:
        return f"❌ خطأ في التحليل: {str(e)}"