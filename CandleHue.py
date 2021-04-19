import time

from python_bitvavo_api.bitvavo import Bitvavo
from phue import Bridge

cryptos = ["ADA-EUR", "AE-EUR", "AION-EUR", "ANT-EUR", "ARK-EUR", "BAT-EUR", "BCH-EUR", "BSV-EUR", "BTC-EUR", "CMT-EUR",
           "DAI-EUR", "DCR-EUR", "DGB-EUR", "ELF-EUR", "ENJ-EUR", "EOS-EUR", "ETC-EUR", "ETH-EUR", "GAS-EUR", "GLM-EUR",
           "GNT-EUR", "HOT-EUR", "ICX-EUR", "IOST-EUR", "KMD-EUR", "LINK-EUR", "LRC-EUR", "LSK-EUR", "LTC-EUR",
           "MIOTA-EUR", "NANO-EUR", "NAS-EUR", "NEO-EUR", "NPXS-EUR", "NULS-EUR", "OMG-EUR", "ONG-EUR", "ONT-EUR",
           "POWR-EUR", "QTUM-EUR", "RDD-EUR", "REQ-EUR", "RVN-EUR", "SNT-EUR", "STEEM-EUR", "STMX-EUR", "STORM-EUR",
           "STRAT-EUR", "STRAX-EUR", "TRX-EUR", "USDC-EUR", "USDT-EUR", "VET-EUR", "VTC-EUR", "VTHO-EUR", "WAVES-EUR",
           "WTC-EUR", "XEM-EUR", "XLM-EUR", "XRP-EUR", "XTZ-EUR", "XVG-EUR", "ZIL-EUR", "ZRX-EUR", "YFI-EUR", "UNI-EUR",
           "COMP-EUR", "YFII-EUR", "BAND-EUR", "SXP-EUR", "REN-EUR", "OXT-EUR", "FET-EUR", "AAVE-EUR", "UMA-EUR",
           "BAL-EUR", "STORJ-EUR", "SUSHI-EUR", "SNX-EUR", "KNC-EUR", "MKR-EUR", "CHZ-EUR", "GNO-EUR", "NMR-EUR",
           "OGN-EUR", "REP-EUR", "RLC-EUR", "RSR-EUR", "TRB-EUR", "UTK-EUR", "LOOM-EUR", "MANA-EUR"]

bitvavo = Bitvavo()

# Connect to the bridge, if it is the first time connecting the LINK button needs to be pressed
bridge = Bridge()
bridge.connect()

# API set-up
bridge.get_api()

# Find the light ID's
lights = list(bridge.get_light_objects(mode='id').keys())


def candle_color(coin, hue, api):
    prev_color = 'yellow'
    while True:
        candle = api.candles(coin, '1m', {})[0]
        open_price = float(candle[1])
        close_price = float(candle[4])

        if close_price >= open_price:
            if prev_color != 'green':
                print('green')
                prev_color = 'green'

                hue.set_light(lights, 'hue', 21845)
        else:
            if prev_color != 'red':
                print('red')
                prev_color = 'red'

                hue.set_light(lights, 'hue', 65535)
        time.sleep(1)


def instant_color(coin, hue, api):
    prev_color = 'yellow'
    prev_value = 0
    while True:
        candle = api.candles(coin, '1m', {})[0]
        value = float(candle[4])

        if value >= prev_value:
            if prev_color != 'green':
                print('green')
                prev_color = 'green'

                hue.set_light(lights, 'hue', 21845)
        else:
            if prev_color != 'red':
                print('red')
                prev_color = 'red'

                hue.set_light(lights, 'hue', 65535)
        prev_value = value
        time.sleep(1)


if __name__ == '__main__':
    # Turn the lights on and up the brightness
    bridge.set_light(lights, 'on', True)
    bridge.set_light(lights, 'bri', 100)

    coin_to_track = input("What coin do you want to track?\n\t")
    coin_to_track += '-EUR'
    while coin_to_track not in cryptos:
        coin_to_track = input(f"Sorry {coin_to_track} is not supported, what coin do you want to track?\n\t")
        coin_to_track += '-EUR'

    candle_color(coin_to_track, bridge, Bitvavo())
    # instant_color(coin_to_track, bridge, Bitvavo())
