import streamlit as st
import json
import os
from sentence_transformers import SentenceTransformer
import base64

# Set page configuration
st.set_page_config(
    page_title="Legal Case Discovery",
    page_icon="⚖️",
    layout="wide",
)

# Custom CSS (same as before)
st.markdown("""
<style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,.1);
        margin-bottom: 20px;
    }
    .highlight {
        background-color: yellow;
        padding: 2px;
    }
    .stImage {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model(model_name):
    return SentenceTransformer(model_name)


def extract_features(text, model):
    return model.encode(text)


def process_query(query, model):
    return extract_features(query, model).tolist()


def search(query, documents, model, top_k=5):
    query_features = process_query(query, model)
    scores = []
    for document in documents:
        score = model.similarity([query_features], [document['features']])[0][0]
        scores.append((document, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


def chunk_text(text, chunk_size=100, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
    return chunks


def extract_relevant_part(query, content, model, chunk_size=256, overlap=50):
    chunks = chunk_text(content, chunk_size, overlap)
    if not chunks:
        return content

    chunk_embeddings = model.encode(chunks)
    query_embedding = extract_features(query, model)
    scores = model.similarity([query_embedding], chunk_embeddings).flatten()
    best_chunk_idx = scores.argmax()
    return chunks[best_chunk_idx]


def load_documents(file_path):
    with open(file_path, 'r') as f:
        documents = json.load(f)
    return documents


def display_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"PDF file not found: {file_path}")
    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")


def main():
    # Display logo
    st.image("img\\logo.png", width=200)  # Replace with your actual logo URL or path

    st.title("Legal Case Discovery")
    st.markdown("<p class='big-font'>Empower your legal research with AI-driven case discovery</p>",
                unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Settings")
    model_name = st.sidebar.selectbox("Embedding Model", ["all-MiniLM-L6-v2", "paraphrase-MiniLM-L6-v2"])
    top_k = st.sidebar.slider("Number of results", 1, 10, 5)

    # Load model
    model = load_model(model_name)

    # Hardcoded index file path
    index_file = "data/my_index_file.json"

    # Query input
    query = st.text_input("Enter your legal query:")

    if st.button("Search"):
        if not os.path.exists(index_file):
            st.error(f"Index file not found: {index_file}")
            return

        documents = load_documents(index_file)
        results = search(query, documents, model, top_k)

        for i, (document, score) in enumerate(results, 1):
            with st.expander(f"Result {i}: {os.path.basename(document['filename'])} (Score: {score:.4f})"):
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)

                # Construct the full path to the PDF
                pdf_path = os.path.join(os.getcwd(), document['filename'])

                st.write(f"**Case Location:** [{os.path.basename(document['filename'])}]({pdf_path})")
                st.write(f"**Score:** {score:.4f}")

                try:
                    relevant_part = extract_relevant_part(query, document['content'], model)
                    highlighted_part = relevant_part.replace(query, f"<span class='highlight'>{query}</span>")
                    st.markdown(f"**Relevant Part:** {highlighted_part}", unsafe_allow_html=True)

                    # Display inline PDF
                    st.write("**Case Document:**")
                    display_pdf(pdf_path)
                except KeyError:
                    # Still try to display the PDF
                    st.write("**Case Document:**")
                    display_pdf(pdf_path)

                st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()