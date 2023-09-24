from uuid import UUID, uuid4

from typing_extensions import override

from src.domain.integration.storage import FileStorageService
from src.domain.notes.models.aggregates.note_upload import NoteUploadAggregate
from src.domain.notes.models.entities.notes import (Note,
                                                    NoteFileProcessingStatus)
from src.domain.notes.models.value_objects.presigned_url_for_upload import \
    PresignedURLForUploadVO
from src.domain.notes.repositories.note_repository import \
    AbstractNoteRepository
from src.domain.notes.services.note_service import AbstractNoteService


class NoteServiceImpl(AbstractNoteService):

    def __init__(self, repository: AbstractNoteRepository, storage_service: FileStorageService) -> None:
        self._repository = repository
        self._storage_service = storage_service

    @override
    def get_note_by_id(self, note_id: UUID) -> Note:
        return self._repository.get_note_by_id(note_id)

    @override
    def create_note(
        self, title: str, content: str, user_id: UUID
    ) -> Note:
        return self._repository.create_note(
            title=title, content=content, user_id=user_id
        )

    @override
    def create_note_by_file(self, title: str, user_id: UUID) -> NoteUploadAggregate:
        file_path = f"notes/{user_id.hex}/{uuid4().hex}.txt"
        note = self._repository.create_note(
            title=title,
            content='',
            user_id=user_id,
            file_path=file_path,
            with_file=False,
            file_processing_status=NoteFileProcessingStatus.PENDING.value,
        )

        expiry = 3600
        url = self._storage_service.get_presigned_upload_url(
            object_name=file_path,
            fields={
                'key': file_path,
                'Content-Type': 'text/plain',
                "x-amz-meta-user_id": f"{user_id}",
                "x-amz-meta-note_id": f"{note.id}",
            },
            conditions=[
                {'Content-Type': 'text/plain'},
                {'acl': 'public-read'},
                {'x-amz-meta-user_id': f"{user_id}"},
                {'x-amz-meta-note_id': f"{note.id}"},
            ],
            expiration=expiry,
        )

        return NoteUploadAggregate(
            note=note,
            presigned_url=PresignedURLForUploadVO(
                url=url.url,
                expiry=expiry,
                extra_fields=url.fields,
            )
        )
