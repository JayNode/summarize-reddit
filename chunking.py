def split_text(text):

    max_chunk_size = 2048

    chunks = []
    current_chunk = ""

    for sentence in text.split("."):

        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
            
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks