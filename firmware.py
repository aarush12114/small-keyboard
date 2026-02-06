import board
import busio
import displayio
import terminalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import MatrixScanner
from kmk.extensions.display import Display, TextEntry

# 1. Initialize Keyboard
keyboard = KMKKeyboard()

# -------------------------------------------------------------------------
# 2. HARDWARE PIN CONFIGURATION
# -------------------------------------------------------------------------

# COLUMN PINS: D3, D6, D7 
col_pins = (board.D3, board.D6, board.D7)

# ROW PINS: D10, D9, D8
row_pins = (board.D10, board.D9, board.D8)

# OLED I2C PINS: SCL=D5, SDA=D4
i2c_bus = busio.I2C(board.D5, board.D4)

# -------------------------------------------------------------------------
# 3. MODULES (Display Only)
# -------------------------------------------------------------------------

driver = None
try:
    import adafruit_displayio_ssd1306
    display_bus = displayio.I2CDisplay(i2c_bus, device_address=0x3C)
    driver = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
    
    display = Display(
        display=driver,
        entries=[
            TextEntry(text='Hack Club!', x=0, y=0, y_anchor='T'),
            TextEntry(text='Layer: ', x=0, y=12, y_anchor='T'),
            TextEntry(text='Base', x=40, y=12, y_anchor='T', layer=0),
        ],
        width=128,
        height=64,
        dim_time=10,
        dim_target=0.1,
        off_time=1200,
        brightness=1
    )
    keyboard.extensions.append(display)
except ImportError:
    print("OLED libraries missing! Screen will be blank.")

# -------------------------------------------------------------------------
# 4. SCANNERS 
# -------------------------------------------------------------------------

keyboard.matrix = MatrixScanner(
    cols=col_pins,
    rows=row_pins,
    diode_orientation=MatrixScanner.DIODE_COL2ROW,
)

# -------------------------------------------------------------------------
# 5. KEYMAP
# -------------------------------------------------------------------------

keyboard.keymap = [
    [
        # Matrix Keys (3x3)
        KC.Q,    KC.W,    KC.E,
        KC.A,    KC.S,    KC.D,
        KC.Z,    KC.X,    KC.C,
    ]
]

if __name__ == '__main__':
    keyboard.go()