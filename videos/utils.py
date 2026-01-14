import hashlib

def compute_sha256_of_uploaded_file(uploaded_file, chunksize=8192):
    file_hash = hashlib.sha256()
    for chunk in uploaded_file.chunks(chunksize):
        file_hash.update(chunk)
    try:
        uploaded_file.seek(0)
    except Exception:
        try:
            uploaded_file.file.seek(0)
        except Exception:
            pass
    return file_hash.hexdigest()
