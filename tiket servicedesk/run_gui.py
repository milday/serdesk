#!/usr/bin/env python3
"""
Launcher untuk GUI ServiceDesk ADIRA
"""

import sys
import os

def main():
    print("🚀 Memulai GUI ServiceDesk ADIRA...")
    print("=" * 40)
    
    try:
        # Import and run the GUI
        from servicedesk_gui import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"❌ Error import: {str(e)}")
        print("Pastikan semua dependencies terinstall:")
        print("  - tkinter (biasanya sudah termasuk dengan Python)")
        print("  - openpyxl")
        print("  - selenium")
        print("  - requests")
        
    except Exception as e:
        print(f"❌ Error menjalankan GUI: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 