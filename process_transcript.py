import json
import re
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def parse_rebel_output(text):
    """
    A more robust parser to handle the REBEL model's output format
    and clean up extra tokens like '</s>' and other tags from the relation string.
    """
    triplets = []
    # This regular expression finds all triplets in the model's output string
    for match in re.finditer(r"<triplet>(.*?)<subj>(.*?)<obj>(.*?)(?:<triplet>|$)", text):
        subject = match.group(1).strip()
        relation = match.group(2).strip()
        obj = match.group(3).strip()
        
        # --- THIS IS THE FINAL FIX, AS YOU REQUESTED ---
        # 1. Remove any end-of-sentence tokens from the relation.
        relation = relation.replace("</s>", "").strip()
        
        # 2. If other tags like <subj> or <obj> are accidentally included in the relation,
        #    take only the text before them.
        if '<subj>' in relation:
            relation = relation.split('<subj>')[0].strip()
        if '<obj>' in relation:
            relation = relation.split('<obj>')[0].strip()
        # --- END OF FIX ---
        
        # 3. Ensure the relation is not empty after cleaning before adding the triplet.
        if relation:
            triplets.append((subject, obj, relation))
            
    return triplets

def run_processing():
    """Loads the model directly to extract relations from raw_test.txt."""
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    device_name = "GPU" if device == "cuda:0" else "CPU"
    print(f"✅ Device set to use {device_name}.")

    try:
        print("🧠 Loading LLM (Babelscape/rebel-large)...")
        tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
        model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
        model.to(device)
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"❌ Failed to load model. Error: {e}")
        return

    try:
        with open('raw_test.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"📖 Read {len(text)} characters from 'raw_test.txt'.")
    except FileNotFoundError:
        print("❌ ERROR: 'raw_test.txt' not found.")
        return

    print("⏳ Starting AI relation extraction...")
    sentences = text.split('.')
    extracted_relations = []

    for i, sentence in enumerate(sentences):
        sentence = sentence.strip().replace("\n", " ")
        if len(sentence) < 20:
            continue

        if i % 10 == 0 and i > 0:
            print(f"  ...processed {i}/{len(sentences)} sentences.")
        
        try:
            inputs = tokenizer(sentence, return_tensors="pt").to(device)
            generated_tokens = model.generate(
                **inputs,
                max_length=256,
                length_penalty=0,
                num_beams=3,
                num_return_sequences=1,
            )
            result_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=False)
            
            triplets = parse_rebel_output(result_text)
            if triplets:
                extracted_relations.extend(triplets)
        except Exception as e:
            print(f"Could not process sentence: '{sentence[:50]}...' Error: {e}")

    unique_relations = list(set(extracted_relations))
    print(f"\n✅ Extraction complete. Found {len(unique_relations)} unique relationships.")

    with open('relations.json', 'w', encoding='utf-8') as f:
        json.dump(unique_relations, f, indent=4)
    print("💾 AI-generated 'relations.json' has been saved.")

if __name__ == '__main__':
    run_processing()