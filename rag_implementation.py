from vertexai.preview import rag
from vertexai.generative_models import GenerativeModel, Tool
import vertexai

PROJECT_ID = "awesome-vigil-472218-b6"
LOCATION = "us-central1"
display_name = "gopi_info_corpus"
path = "personal_data.txt"

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Create RAG corpus using the correct function
embedding_model_config = rag.EmbeddingModelConfig(
    publisher_model="publishers/google/models/text-embedding-005"
)

rag_corpus = rag.create_corpus(
    display_name=display_name,
    embedding_model_config=embedding_model_config
)

# Import files
rag.import_files(
    corpus_name=rag_corpus.name,
    paths=[path],       # make sure `paths` is a list
    transformation_config=rag.TransformationConfig(
        chunking_config=rag.ChunkingConfig(
            chunk_size=256,
            chunk_overlap=50,
        )
    ),
)

# Other parts remain as you had

rag_retrieval_config = rag.RagRetrievalConfig(
    top_k=3, 
    filter=rag.Filter(vector_distance_threshold=0.5),
)

rag_retrieval_tool = Tool.from_retrieval(
    retrieval=rag.Retrieval(
        source=rag.VertexRagStore(
            rag_resources=[
                rag.RagResource(rag_corpus=rag_corpus.name)
            ],
            rag_retrieval_config=rag_retrieval_config,
        )
    )
)

rag_model = GenerativeModel(
    model_name="gemini-3-12b-it", tools=[rag_retrieval_tool]
)

response = rag_model.generate_content("What should I wear to office today?")
print(response.text)
print(response.citations)
