def create_raw_text_file():
    """
    Reads the original test.txt file, removes the pre-labeled answers,
    and saves the clean sentences to a new 'raw_text.txt' file.
    """
    print("🧹 Cleaning the input file...")
    try:
        with open('test.txt', 'r', encoding='utf-8') as infile, \
             open('raw_text.txt', 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                # Take only the part of the line before the first '|'
                sentence = line.split('|')[0].strip()
                
                # Write the cleaned sentence to the new file if it's not empty
                if sentence:
                    outfile.write(sentence + '\n')
        
        print("✅ Successfully created clean 'raw_text.txt' file.")
        print("➡️ You can now proceed to run 'process_transcript.py'.")

    except FileNotFoundError:
        print("❌ ERROR: 'test.txt' not found in this directory.")

if __name__ == '__main__':
    create_raw_text_file()