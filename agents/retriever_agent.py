
import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import os

class RetrieverAgent:
    def __init__(self, docs_path="docs_data", index_path="vector_index"):
        import os
        project_root = os.path.dirname(os.path.dirname(__file__))  
        self.docs_path = os.path.join(project_root, docs_path)
        self.index_path = os.path.join(project_root, index_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []

        if not os.path.exists(self.index_path):
            os.makedirs(self.index_path)

        self.load_or_create_index()


    def load_or_create_index(self):
        index_file = os.path.join(self.index_path, "faiss.index")
        meta_file = os.path.join(self.index_path, "docs.pkl")

        if os.path.exists(index_file) and os.path.exists(meta_file):
            self.index = faiss.read_index(index_file)
            with open(meta_file, "rb") as f:
                self.documents = pickle.load(f)
        else:
            self.create_index()

    def create_index(self):
        texts = []
        for filename in os.listdir(self.docs_path):
            file_path = os.path.join(self.docs_path, filename)
            if filename.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    texts.append(content)
                    self.documents.append({"filename": filename, "content": content})

        embeddings = self.model.encode(texts, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

      
        faiss.write_index(self.index, os.path.join(self.index_path, "faiss.index"))
        with open(os.path.join(self.index_path, "docs.pkl"), "wb") as f:
            pickle.dump(self.documents, f)

    def query(self, question, top_k=2):
        question_embedding = self.model.encode([question])
        D, I = self.index.search(question_embedding, top_k)

        results = []
        for i in I[0]:
            if i < len(self.documents):
                results.append(self.documents[i]["content"][:500])  

        return results


if __name__ == "__main__":
    agent = RetrieverAgent()
    response = agent.query("What is Apple's revenue?")
    print("\n".join(response))
