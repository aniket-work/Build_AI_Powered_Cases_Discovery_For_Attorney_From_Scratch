import os
import json
import multiprocessing
import glob
from sentence_transformers import SentenceTransformer
from tqdm.auto import tqdm
from pypdf import PdfReader
from joblib import Parallel, delayed
import torch


def load_config(config_path='config/indexer_config.json'):
    """Load configuration from JSON file."""
    with open(config_path, 'r') as config_file:
        return json.load(config_file)


def read_file_content(filename):
    """Read content from text or PDF files."""
    try:
        if filename.endswith('.txt'):
            with open(filename, 'r', errors='ignore') as file:
                return file.read()
        elif filename.endswith('.pdf'):
            reader = PdfReader(filename)
            return ' '.join(page.extract_text() for page in reader.pages)
        else:
            raise ValueError(f"Unsupported file format: {filename}")
    except Exception as e:
        print(f"Error reading file {filename}: {str(e)}")
        return ""


def create_text_chunks(text, chunk_size=512, overlap=50):
    """Split text into overlapping chunks."""
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size - overlap)]


def encode_document(filename, model, config, content):
    """Encode document content into chunks with embeddings."""
    chunks = create_text_chunks(content, config['chunk_size'], config['overlap'])
    documents = []

    for i, chunk in enumerate(chunks):
        try:
            features = model.encode(chunk, show_progress_bar=False).tolist()
            document = {
                'filename': filename,
                'chunk': i,
                'features': features
            }
            if config['add_file_content']:
                document['content'] = chunk
            documents.append(document)
        except Exception as e:
            print(f"Error encoding chunk {i} of {filename}: {str(e)}")

    return documents


def process_file(filename, model, config):
    """Process a single file: read content and encode document."""
    try:
        content = read_file_content(filename)
        return encode_document(filename, model, config, content)
    except Exception as e:
        print(f"Error processing file {filename}: {str(e)}")
        return []


def main():
    multiprocessing.set_start_method('spawn', force=True)

    config = load_config()

    # Use CPU for encoding to avoid CUDA memory issues
    device = torch.device("cpu")
    model = SentenceTransformer(config['model']).to(device)
    print(f"Using device: {device}")

    all_files = glob.glob(os.path.join(config['directory_path'], '**'), recursive=True)
    files_to_process = [f for f in all_files if os.path.isfile(f) and f.endswith(('.txt', '.pdf'))]

    # Process files in batches to manage memory
    batch_size = 10
    results = []
    for i in range(0, len(files_to_process), batch_size):
        batch = files_to_process[i:i + batch_size]
        batch_results = Parallel(n_jobs=min(config['njobs'], len(batch)), backend='multiprocessing')(
            delayed(process_file)(filename, model, config)
            for filename in tqdm(batch, desc=f"Processing batch {i // batch_size + 1}")
        )
        results.extend(batch_results)

    documents = [doc for result in results for doc in result]

    with open(os.path.join('data', config['index_file_name']), 'w') as f:
        json.dump(documents, f)

    print(f"Indexing complete. Output saved to data/{config['index_file_name']}")


if __name__ == '__main__':
    main()