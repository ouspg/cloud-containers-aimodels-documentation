from api.rag import RagService

rag = RagService()
context, sources = rag.query("Who is Wainamoinen?")
print("Context:\n", context)
print("Sources:", sources)
