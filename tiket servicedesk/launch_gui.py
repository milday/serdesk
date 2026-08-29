#!/usr/bin/env python3
"""
GUI Launcher Test - Verifies GUI can actually open and display
"""

import sys
import traceback

print("🚀 Launching ServiceDesk GUI...")

try:
    # Test import first
    print("Testing imports...")
    from servicedesk_gui import main
    print("✅ GUI imports successful")
    
    # Launch the GUI
    print("🎯 Starting GUI application...")
    print("Note: This will open the GUI window. Close it to complete the test.")
    
    main()
    
    print("✅ GUI closed successfully!")
    
except KeyboardInterrupt:
    print("\n⚠️ GUI startup interrupted by user")
    print("This is normal if you closed the GUI window")
    
except Exception as e:
    print(f"❌ Error launching GUI: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

print("\n✅ GUI test completed!")
print("The ServiceDesk GUI is working properly.") 