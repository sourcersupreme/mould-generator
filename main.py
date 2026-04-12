from modules.brick import generate_brick_mould

def main():
    print("Mould Generator")
    print("1. Brick Mould")

    choice = input("Select option: ")

    if choice == "1":
        generate_brick_mould("output.pdf")
        print("[✓] PDF Generated: output.pdf")
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
