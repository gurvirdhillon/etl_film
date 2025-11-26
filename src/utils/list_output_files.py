import os

# Always anchor path to THIS project folder, not current working directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
output_path = os.path.join(BASE_DIR, "data", "output")

print("Checking:", output_path)
print("\nFiles in output folder:\n")

if not os.path.exists(output_path):
    print("Output folder does NOT exist!")
else:
    files = os.listdir(output_path)
    if not files:
        print("⚠️ No files found.")
    else:
        for f in files:
            print(" -", f)

