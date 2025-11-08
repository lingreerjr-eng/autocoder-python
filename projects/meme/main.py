import asyncio
from scanner import MemecoinScanner
from analyzer import MemecoinAnalyzer
from notifier import Notifier

async def main():
    print("Starting Memecoin Scanner...")
    
    # Initialize components
    scanner = MemecoinScanner()
    analyzer = MemecoinAnalyzer()
    notifier = Notifier()
    
    # Scan for new memecoins
    print("Scanning for new memecoins...")
    new_coins = await scanner.scan_new_tokens()
    
    # Analyze each coin
    print(f"Analyzing {len(new_coins)} new memecoins...")
    analyzed_coins = []
    
    for coin in new_coins:
        try:
            analysis = await analyzer.analyze_token(coin)
            if analysis:
                analyzed_coins.append(analysis)
        except Exception as e:
            print(f"Error analyzing {coin.get('symbol', 'Unknown')}: {e}")
    
    # Sort by profit potential score
    analyzed_coins.sort(key=lambda x: x.get('profit_score', 0), reverse=True)
    
    # Get top opportunities
    top_opportunities = analyzed_coins[:10]
    
    # Display results
    print("\nTop Memecoin Opportunities:")
    print("=" * 50)
    for i, coin in enumerate(top_opportunities, 1):
        print(f"{i}. {coin['name']} ({coin['symbol']}) - Address: {coin['address']}")
        print(f"   Score: {coin['profit_score']:.2f}/100")
        print(f"   Market Cap: ${coin['market_cap']:,.2f}")
        print(f"   Dev Allocation: {coin['dev_allocation']:.1f}%")
        print(f"   Rugged: {'Yes' if coin['is_rugged'] else 'No'}")
        print(f"   Liquidity: ${coin['liquidity']:,.2f}")
        print(f"   Volatility: {coin['volatility']:.2f}%")
        print(f"   Bundled: {'Yes' if coin['is_bundled'] else 'No'}")
        print()
    
    # Send notifications if any high potential coins found
    high_potential = [coin for coin in top_opportunities if coin['profit_score'] > 80]
    if high_potential:
        await notifier.send_alert(high_potential)

if __name__ == "__main__":
    asyncio.run(main())
