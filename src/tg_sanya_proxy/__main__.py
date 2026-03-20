import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tg_sanya_proxy.app import main

if __name__ == "__main__":
    main().main_loop()
