import sys

print('start of Python script')

def main():
    # Access filenames from command line arguments
    if len(sys.argv) > 1:
        file_name = sys.argv[1:]
        print("File name:", file_name)
        
        # Continue with your Python script logic using file_names

if __name__ == "__main__":
    main()
