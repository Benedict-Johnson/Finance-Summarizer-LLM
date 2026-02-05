from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from transformers import pipeline
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# --- GLOBAL VARIABLES ---
RELATIONSHIPS = []
print("🧠 Loading real-time LLM (google/flan-t5-large)... This may take a moment.")
llm = pipeline("text2text-generation", model="google/flan-t5-large", device=-1)
print("✅ Real-time LLM is ready.")

@app.route('/query', methods=['GET'])
def query_entities():
    user_prompt = request.args.get('q', '')
    
    if not user_prompt:
        return jsonify({"error": "Query parameter 'q' is required."}), 400

    # --- TASK 1: Extract Keyword ---
    keyword_prompt = f"""Extract the primary company or person's name from this question: "{user_prompt}" Name:"""
    entity_name = llm(keyword_prompt, max_new_tokens=10)[0]['generated_text'].strip().lower()
    print(f"🤖 LLM identified keyword: '{entity_name}'")

    # --- TASK 2: Retrieve and De-duplicate Data ---
    relevant_relations = list(set(tuple(i) for i in [
        rel for rel in RELATIONSHIPS 
        if entity_name in rel[0].lower() or entity_name in rel[1].lower()
    ]))
    
    if not relevant_relations:
        summary = f"I couldn't find any specific relationships for '{entity_name}' in the document."
    else:
        # --- TASK 3: Generate a High-Quality Summary ---
        
        # Group facts by relationship type for a much cleaner input
        grouped_facts = defaultdict(list)
        for sub, obj, rel in relevant_relations:
            # Add the entity that is NOT the one being searched for
            if entity_name in sub.lower():
                grouped_facts[rel].append(obj)
            else:
                grouped_facts[rel].append(sub)

        # ** THIS IS THE KEY FIX **: Create a clean, bulleted list for the AI
        fact_list_for_prompt = []
        for rel, entities in grouped_facts.items():
            # De-duplicate entities for each relationship
            unique_entities = ", ".join(sorted(list(set(entities))))
            fact_list_for_prompt.append(f"- As a {rel}: {unique_entities}")
        
        context = "\n".join(fact_list_for_prompt)

        # A much clearer and more direct prompt
        summary_prompt = f"""
        Write a brief, professional summary based on the following points about {entity_name.title()}.

        Key Points:
        {context}

        Summary Paragraph:
        """
        summary = llm(summary_prompt, max_new_tokens=150)[0]['generated_text']
        print(f"🤖 AI-generated summary: '{summary}'")

    return jsonify({
        "edges": relevant_relations,
        "summary": summary
    })

def load_preprocessed_data():
    global RELATIONSHIPS
    try:
        with open('relations.json', 'r', encoding='utf-8') as f:
            RELATIONSHIPS = json.load(f)
        print(f"✅ Knowledge Base loaded with {len(RELATIONSHIPS)} relationships.")
    except FileNotFoundError:
        print("❌ WARNING: relations.json not found. Run 'convert_data.py' first.")
        RELATIONSHIPS = []

if __name__ == '__main__':
    load_preprocessed_data()
    app.run(debug=False, port=5000)