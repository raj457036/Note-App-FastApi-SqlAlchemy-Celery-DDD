import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.core.di.injector import RootContainer
from src.domain.notes.dtos import CreateNoteByFileDTO, CreateNoteDTO
from src.domain.notes.models.aggregates.note_upload import NoteUploadAggregate
from src.domain.notes.models.entities.notes import Note
from src.domain.notes.usecases.create_note import CreateNoteUseCase
from src.domain.notes.usecases.create_note_by_file import \
    CreateNoteByFileUseCase
from src.domain.notes.usecases.get_note_by_id import GetNoteByIDUseCase
from src.infra.common.integration.storage.s3_storage_provider import (
    S3SignedUrlResponse, S3StorageProvider)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notes")


@router.post("/", response_model=Note)
@inject
def create_note(
    dto: CreateNoteDTO,
    create_note_usecase: CreateNoteUseCase = Depends(
        Provide[RootContainer.note.create_note]),
):
    logger.info(f"Creating note {dto}")
    note = create_note_usecase.execute(dto)
    return note


@router.get("/{note_id}", response_model=Note)
@inject
def get_note_by_id(
    note_id: UUID,
    get_note_by_id_usecase: GetNoteByIDUseCase = Depends(
        Provide[RootContainer.note.get_note_by_id]),
) -> Note:
    logger.info(f"Getting note {note_id}")
    note = get_note_by_id_usecase.execute(note_id)
    return note


@router.post(
    "/create_by_file",
    # response_model=NoteUploadAggregate
    response_model=S3SignedUrlResponse
)
@inject
def create_note_by_file(
    dto: CreateNoteByFileDTO,
    create_note_by_file_usecase: CreateNoteByFileUseCase = Depends(
        Provide[RootContainer.note.create_note_by_file]),
    file_storage: S3StorageProvider = Depends(
        Provide(RootContainer.file_storage_provider)),
):
    logger.info(f"Creating note by file {dto}")
    # note = create_note_by_file_usecase.execute(dto)
    # return note
    url = file_storage.get_presigned_upload_url(
        object_name="test.txt",
        expiration=3600,
        conditions=[
            {'x-amz-meta-document_id': 'doc_id_1'}
        ],
        fields={
            "x-amz-meta-document_id": "doc_id_1",
        }
    )
    return url
