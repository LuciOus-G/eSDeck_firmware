import os

metadata = {
    "port": "COM7",
    "baud": "115200"
}

folder_root = "src"

def main():
    files = os.listdir("src")
    
    for f in files:
        os.system(f"cd {folder_root} && conda activate micropython && ampy --port {metadata['port']} --baud {metadata['baud']} put {f}")
    
    
    
if __name__ == "__main__":
    main() 