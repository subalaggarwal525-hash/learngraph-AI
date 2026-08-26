import os, shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import DocumentModel, DocumentChunkModel, CourseModel
from backend.app.documents.parser import DocumentParser
from backend.app.rag.vector_store import global_vector_store

router = APIRouter(prefix="/api/documents", tags=["documents"])
UPLOAD_DIR = "./uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(course_id: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed = DocumentParser.parse_file(file_path, file.filename)
    sections = parsed.get("sections", [])

    db_doc = DocumentModel(course_id=course_id, filename=file.filename, file_type=file.content_type or "application/octet-stream", file_size=os.path.getsize(file_path))
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    for idx, s in enumerate(sections):
        db.add(DocumentChunkModel(document_id=db_doc.id, chunk_index=idx, section_title=s.get("section_title", f"Chunk {idx+1}"), content=s.get("content", "")))
    db.commit()

    global_vector_store.add_chunks(course_id, db_doc.id, sections)
    return {"document_id": db_doc.id, "filename": file.filename, "total_sections": len(sections), "status": "indexed_in_rag"}
