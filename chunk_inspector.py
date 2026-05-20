from rag_loader import load_chunks

chunks = load_chunks()

print("TOTAL CHUNKS:", len(chunks))
print("="*60)

for i, c in enumerate(chunks[:20], 1):
    t = c.lower()
    print(f"\n--- CHUNK {i} ---")
    print("lakehouse:", "lakehouse" in t,
          "warehouse:", "warehouse" in t,
          "onelake:", "onelake" in t,
          "shortcut:", "shortcut" in t)
    print(c[:300].replace("\n", " "))
