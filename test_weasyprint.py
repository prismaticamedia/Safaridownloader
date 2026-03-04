import sys
import ctypes.util

# Try hardcoding the path directly
path = '/opt/homebrew/lib/libgobject-2.0.dylib'

try:
    # Directly test ctypes
    import ctypes
    lib = ctypes.CDLL(path)
    print("Success loading library!")
    
    # Try importing weasyprint again with ctypes patched? No need, let's just see if CDLL works.
except Exception as e:
    print(f"Failed to load: {e}")
