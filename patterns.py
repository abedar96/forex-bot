def detect_patterns(df):
    recent = df.tail(5)
    opens = recent["Open"]
    closes = recent["Close"]
    highs = recent["High"]
    lows = recent["Low"]
    
    # Bullish Engulfing
    if len(recent) >= 2:
        prev, curr = -2, -1
        if (closes.iloc[prev] < opens.iloc[prev] and
            closes.iloc[curr] > opens.iloc[curr] and
            closes.iloc[curr] > opens.iloc[prev] and
            opens.iloc[curr] < closes.iloc[prev]):
            return "Bullish Engulfing (التشابك الصاعد)"
    
    # Bearish Engulfing
    if len(recent) >= 2:
        prev, curr = -2, -1
        if (closes.iloc[prev] > opens.iloc[prev] and
            closes.iloc[curr] < opens.iloc[curr] and
            closes.iloc[curr] < opens.iloc[prev] and
            opens.iloc[curr] > closes.iloc[prev]):
            return "Bearish Engulfing (التشابك الهابط)"
    
    # Hammer
    if len(recent) >= 1:
        candle = recent.iloc[-1]
        body_size = abs(candle["Close"] - candle["Open"])
        lower_wick = min(candle["Open"], candle["Close"]) - candle["Low"]
        upper_wick = candle["High"] - max(candle["Open"], candle["Close"])
        
        if (lower_wick > 2 * body_size and 
            upper_wick < body_size and
            candle["Close"] > candle["Open"]):
            return "Hammer (المطرقة)"
    
    # Shooting Star
    if len(recent) >= 1:
        candle = recent.iloc[-1]
        body_size = abs(candle["Close"] - candle["Open"])
        lower_wick = min(candle["Open"], candle["Close"]) - candle["Low"]
        upper_wick = candle["High"] - max(candle["Open"], candle["Close"])
        
        if (upper_wick > 2 * body_size and 
            lower_wick < body_size and
            candle["Close"] < candle["Open"]):
            return "Shooting Star (النجمة الهابط)"
    
    # Morning Star
    if len(recent) >= 3:
        first, second, third = -3, -2, -1
        if (closes.iloc[first] < opens.iloc[first] and
            abs(closes.iloc[second] - opens.iloc[second])/(highs.iloc[second] - lows.iloc[second]) < 0.3 and
            closes.iloc[third] > opens.iloc[third] and
            closes.iloc[third] > opens.iloc[first]):
            return "Morning Star (نجمة الصباح)"
    
    return None
