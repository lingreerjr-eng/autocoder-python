import asyncio
import random
from typing import Dict, Optional

class MemecoinAnalyzer:
    async def analyze_token(self, token: Dict) -> Optional[Dict]:
        # Simulate API delay
        await asyncio.sleep(0.5)
        
        # Generate mock analysis data
        market_cap = random.uniform(100000, 5000000)
        liquidity = market_cap * random.uniform(0.1, 0.5)
        dev_allocation = random.uniform(0, 15)
        volatility = random.uniform(5, 50)
        
        # Determine if token is rugged (simplified logic)
        is_rugged = random.random() < 0.3  # 30% chance
        
        # Determine if token is bundled (simplified logic)
        is_bundled = random.random() < 0.2  # 20% chance
        
        # Calculate profit score based on multiple factors
        score = self._calculate_profit_score(
            market_cap, 
            dev_allocation, 
            is_rugged, 
            liquidity, 
            volatility,
            is_bundled
        )
        
        return {
            "address": token["address"],
            "name": token["name"],
            "symbol": token["symbol"],
            "market_cap": market_cap,
            "liquidity": liquidity,
            "dev_allocation": dev_allocation,
            "is_rugged": is_rugged,
            "is_bundled": is_bundled,
            "volatility": volatility,
            "profit_score": score
        }
    
    def _calculate_profit_score(self, market_cap: float, dev_allocation: float, 
                               is_rugged: bool, liquidity: float, 
                               volatility: float, is_bundled: bool) -> float:
        # Base score
        score = 50.0
        
        # Market cap factor (optimal between $500K and $2M)
        if 500000 <= market_cap <= 2000000:
            score += 20
        elif market_cap < 500000:
            score += 10
        
        # Dev allocation factor (lower is better)
        if dev_allocation < 5:
            score += 15
        elif dev_allocation < 10:
            score += 5
        
        # Rugged factor
        if is_rugged:
            score -= 50
        
        # Liquidity factor (higher is better)
        liquidity_ratio = liquidity / market_cap if market_cap > 0 else 0
        if liquidity_ratio > 0.3:
            score += 15
        elif liquidity_ratio > 0.1:
            score += 5
        
        # Volatility factor (moderate is preferred)
        if 10 <= volatility <= 30:
            score += 10
        elif volatility > 30:
            score -= 5
        
        # Bundled factor
        if is_bundled:
            score -= 20
        
        # Ensure score is within bounds
        return max(0, min(100, score))
