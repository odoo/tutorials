import os

def merge_all_files_in_folder(folder_path="."):
    """Recursively merge all text files inside the current folder into one file."""
    output_file = os.path.join(folder_path, "merged_output.txt")  

    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, _, files in os.walk(folder_path):
            for file in sorted(files):
                file_path = os.path.join(root, file)

                # खुद output file को skip करें
                if file == "merged_output.txt":
                    continue  

                # सिर्फ text-based files ही merge करें (case-insensitive check)
                if not file.lower().endswith((".txt", ".py", ".xml", ".csv", ".md", ".json", ".html", ".css", ".js")):
                    print(f"⚠️ Skipping non-text file: {file_path}")
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                        outfile.write(f"\n\n# ----- Start of {file} ----- #\n")
                        for line in infile:  # Memory-efficient reading
                            outfile.write(line)
                        outfile.write(f"\n\n# ----- End of {file} ----- #\n")
                except Exception as e:
                    print(f"❌ Error reading {file_path}: {e}")

    print(f"✅ All files merged into: {output_file}")

# Run the script inside the current folder
merge_all_files_in_folder(os.getcwd())  
