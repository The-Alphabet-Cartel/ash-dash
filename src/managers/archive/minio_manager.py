"""
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Reveal   → Surface crisis alerts and user escalation patterns in real-time
    Enable   → Equip Crisis Response Teams with tools for swift intervention
    Clarify  → Translate detection data into actionable intelligence
    Protect  → Safeguard our LGBTQIA+ community through vigilant oversight

============================================================================
MinIO Manager - S3-compatible object storage client for session archives
----------------------------------------------------------------------------
FILE VERSION: v5.0-8-8.1-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 8 - Archive Infrastructure
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Connect to MinIO on Syn VM (10.20.30.202)
- Upload encrypted session archives
- Download and list archived sessions
- Provide health checks and connection management
- Handle bucket operations for ash-archives, ash-documents, ash-exports

MINIO BUCKETS:
- ash-archives: Encrypted crisis session archives
- ash-documents: Document backups
- ash-exports: PDF exports and reports

USAGE:
    minio_manager = await create_minio_manager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
        logging_manager=logging_manager,
    )
    
    # Upload archive
    await minio_manager.upload_archive(session_id, encrypted_data)
    
    # List archives
    archives = await minio_manager.list_archives(prefix="2026-01")
    
    # Download archive
    data = await minio_manager.download_archive(session_id)
"""

import asyncio
import io
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, BinaryIO

from minio import Minio
from minio.error import S3Error
from urllib3.exceptions import MaxRetryError

__version__ = "v5.0-8-8.1-1"


class MinIOManager:
    """
    S3-compatible object storage client for session archives.

    Connects to MinIO on Syn VM to store encrypted session data,
    documents, and PDF exports.

    Attributes:
        _client: MinIO client instance
        _config: MinIO configuration
        _logger: Logging manager
        _connected: Connection status flag
    """

    # Default bucket names
    BUCKET_ARCHIVES = "ash-archives"
    BUCKET_DOCUMENTS = "ash-documents"
    BUCKET_EXPORTS = "ash-exports"

    def __init__(
        self,
        config: Dict[str, Any],
        access_key: Optional[str],
        secret_key: Optional[str],
        logging_manager,
    ):
        """
        Initialize MinIOManager (do not call directly, use factory).

        Args:
            config: MinIO configuration dictionary
            access_key: MinIO access key (from secrets)
            secret_key: MinIO secret key (from secrets)
            logging_manager: LoggingManager instance
        """
        self._config = config
        self._access_key = access_key
        self._secret_key = secret_key
        self._logging_manager = logging_manager
        self._logger = logging_manager.get_logger("minio")
        self._client: Optional[Minio] = None
        self._connected = False

        # Get bucket names from config
        self._bucket_archives = config.get("bucket_archives", self.BUCKET_ARCHIVES)
        self._bucket_documents = config.get("bucket_documents", self.BUCKET_DOCUMENTS)
        self._bucket_exports = config.get("bucket_exports", self.BUCKET_EXPORTS)

    # =========================================================================
    # Connection Management
    # =========================================================================

    async def connect(self) -> None:
        """
        Establish connection to MinIO.

        Creates MinIO client and verifies connectivity.

        Raises:
            ConnectionError: If connection fails
        """
        endpoint = self._config.get("endpoint", "10.20.30.202")
        port = self._config.get("port", 30884)
        secure = self._config.get("secure", False)

        self._logger.info(f"🔌 Connecting to MinIO at {endpoint}:{port}")

        if not self._access_key or not self._secret_key:
            self._logger.error("❌ MinIO credentials not configured")
            raise ConnectionError("MinIO credentials not configured")

        try:
            # Create MinIO client
            self._client = Minio(
                endpoint=f"{endpoint}:{port}",
                access_key=self._access_key,
                secret_key=self._secret_key,
                secure=secure,
            )

            # Test connection by listing buckets
            await asyncio.to_thread(self._client.list_buckets)
            self._connected = True
            self._logger.info("✅ MinIO connection established")

            # Ensure buckets exist
            await self._ensure_buckets()

        except (S3Error, MaxRetryError) as e:
            self._connected = False
            self._logger.error(f"❌ MinIO connection failed: {e}")
            raise ConnectionError(f"MinIO connection failed: {e}")

    async def _ensure_buckets(self) -> None:
        """Ensure required buckets exist."""
        buckets = [
            self._bucket_archives,
            self._bucket_documents,
            self._bucket_exports,
        ]

        for bucket in buckets:
            try:
                exists = await asyncio.to_thread(
                    self._client.bucket_exists, bucket
                )
                if exists:
                    self._logger.debug(f"✓ Bucket exists: {bucket}")
                else:
                    self._logger.warning(f"⚠️ Bucket missing: {bucket}")
            except S3Error as e:
                self._logger.warning(f"⚠️ Could not check bucket {bucket}: {e}")

    async def close(self) -> None:
        """Close MinIO connection."""
        self._client = None
        self._connected = False
        self._logger.info("🔌 MinIO connection closed")

    async def reconnect(self) -> None:
        """Reconnect to MinIO."""
        await self.close()
        await self.connect()

    @property
    def is_connected(self) -> bool:
        """Check if connected to MinIO."""
        return self._connected

    # =========================================================================
    # Health Check
    # =========================================================================

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform MinIO health check.

        Returns:
            Health status dictionary with latency and bucket info
        """
        if not self._client:
            return {
                "healthy": False,
                "error": "MinIO client not initialized",
            }

        try:
            start = time.perf_counter()
            buckets = await asyncio.to_thread(self._client.list_buckets)
            latency_ms = (time.perf_counter() - start) * 1000

            bucket_names = [b.name for b in buckets]

            return {
                "healthy": True,
                "latency_ms": round(latency_ms, 2),
                "buckets": bucket_names,
                "bucket_count": len(buckets),
                "endpoint": f"{self._config.get('endpoint')}:{self._config.get('port')}",
            }

        except (S3Error, MaxRetryError) as e:
            self._connected = False
            return {
                "healthy": False,
                "error": str(e),
            }

    # =========================================================================
    # Archive Operations (ash-archives bucket)
    # =========================================================================

    async def upload_archive(
        self,
        object_name: str,
        data: bytes,
        metadata: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Upload encrypted archive data.

        Args:
            object_name: Object key (e.g., "2026/01/session_123.enc")
            data: Encrypted data bytes
            metadata: Optional metadata dictionary

        Returns:
            True if upload successful
        """
        if not self._client:
            self._logger.error("MinIO client not initialized")
            return False

        try:
            data_stream = io.BytesIO(data)
            
            await asyncio.to_thread(
                self._client.put_object,
                self._bucket_archives,
                object_name,
                data_stream,
                length=len(data),
                content_type="application/octet-stream",
                metadata=metadata or {},
            )

            self._logger.debug(f"✓ Uploaded archive: {object_name}")
            return True

        except S3Error as e:
            self._logger.error(f"❌ Upload failed for {object_name}: {e}")
            return False

    async def download_archive(
        self,
        object_name: str,
    ) -> Optional[bytes]:
        """
        Download encrypted archive data.

        Args:
            object_name: Object key to download

        Returns:
            Encrypted data bytes or None if not found
        """
        if not self._client:
            return None

        try:
            response = await asyncio.to_thread(
                self._client.get_object,
                self._bucket_archives,
                object_name,
            )
            data = response.read()
            response.close()
            response.release_conn()

            self._logger.debug(f"✓ Downloaded archive: {object_name}")
            return data

        except S3Error as e:
            if e.code == "NoSuchKey":
                self._logger.debug(f"Archive not found: {object_name}")
            else:
                self._logger.error(f"❌ Download failed for {object_name}: {e}")
            return None

    async def list_archives(
        self,
        prefix: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        List archives with optional prefix filter.

        Args:
            prefix: Object key prefix (e.g., "2026/01/")
            limit: Maximum number of results

        Returns:
            List of archive metadata dictionaries
        """
        if not self._client:
            return []

        try:
            objects = await asyncio.to_thread(
                self._client.list_objects,
                self._bucket_archives,
                prefix=prefix,
                recursive=True,
            )

            archives = []
            for obj in objects:
                if len(archives) >= limit:
                    break
                archives.append({
                    "name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified,
                    "etag": obj.etag,
                })

            self._logger.debug(f"Listed {len(archives)} archives (prefix={prefix})")
            return archives

        except S3Error as e:
            self._logger.error(f"❌ List failed: {e}")
            return []

    async def delete_archive(
        self,
        object_name: str,
    ) -> bool:
        """
        Delete an archive.

        Args:
            object_name: Object key to delete

        Returns:
            True if deletion successful
        """
        if not self._client:
            return False

        try:
            await asyncio.to_thread(
                self._client.remove_object,
                self._bucket_archives,
                object_name,
            )

            self._logger.debug(f"✓ Deleted archive: {object_name}")
            return True

        except S3Error as e:
            self._logger.error(f"❌ Delete failed for {object_name}: {e}")
            return False

    async def archive_exists(
        self,
        object_name: str,
    ) -> bool:
        """
        Check if an archive exists.

        Args:
            object_name: Object key to check

        Returns:
            True if archive exists
        """
        if not self._client:
            return False

        try:
            await asyncio.to_thread(
                self._client.stat_object,
                self._bucket_archives,
                object_name,
            )
            return True

        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            self._logger.error(f"❌ Stat failed for {object_name}: {e}")
            return False

    # =========================================================================
    # Document Operations (ash-documents bucket)
    # =========================================================================

    async def upload_document(
        self,
        object_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Upload a document to the documents bucket.

        Args:
            object_name: Object key
            data: Document data bytes
            content_type: MIME type
            metadata: Optional metadata

        Returns:
            True if upload successful
        """
        if not self._client:
            return False

        try:
            data_stream = io.BytesIO(data)
            
            await asyncio.to_thread(
                self._client.put_object,
                self._bucket_documents,
                object_name,
                data_stream,
                length=len(data),
                content_type=content_type,
                metadata=metadata or {},
            )

            self._logger.debug(f"✓ Uploaded document: {object_name}")
            return True

        except S3Error as e:
            self._logger.error(f"❌ Document upload failed for {object_name}: {e}")
            return False

    async def download_document(
        self,
        object_name: str,
    ) -> Optional[bytes]:
        """
        Download a document.

        Args:
            object_name: Object key

        Returns:
            Document data bytes or None
        """
        if not self._client:
            return None

        try:
            response = await asyncio.to_thread(
                self._client.get_object,
                self._bucket_documents,
                object_name,
            )
            data = response.read()
            response.close()
            response.release_conn()
            return data

        except S3Error as e:
            if e.code != "NoSuchKey":
                self._logger.error(f"❌ Document download failed: {e}")
            return None

    # =========================================================================
    # Export Operations (ash-exports bucket)
    # =========================================================================

    async def upload_export(
        self,
        object_name: str,
        data: bytes,
        content_type: str = "application/pdf",
        metadata: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Upload a PDF export.

        Args:
            object_name: Object key (e.g., "reports/2026-01-09_summary.pdf")
            data: PDF data bytes
            content_type: MIME type (default: application/pdf)
            metadata: Optional metadata

        Returns:
            True if upload successful
        """
        if not self._client:
            return False

        try:
            data_stream = io.BytesIO(data)
            
            await asyncio.to_thread(
                self._client.put_object,
                self._bucket_exports,
                object_name,
                data_stream,
                length=len(data),
                content_type=content_type,
                metadata=metadata or {},
            )

            self._logger.debug(f"✓ Uploaded export: {object_name}")
            return True

        except S3Error as e:
            self._logger.error(f"❌ Export upload failed for {object_name}: {e}")
            return False

    async def download_export(
        self,
        object_name: str,
    ) -> Optional[bytes]:
        """
        Download a PDF export.

        Args:
            object_name: Object key

        Returns:
            PDF data bytes or None
        """
        if not self._client:
            return None

        try:
            response = await asyncio.to_thread(
                self._client.get_object,
                self._bucket_exports,
                object_name,
            )
            data = response.read()
            response.close()
            response.release_conn()
            return data

        except S3Error as e:
            if e.code != "NoSuchKey":
                self._logger.error(f"❌ Export download failed: {e}")
            return None

    async def list_exports(
        self,
        prefix: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        List exports with optional prefix filter.

        Args:
            prefix: Object key prefix
            limit: Maximum number of results

        Returns:
            List of export metadata dictionaries
        """
        if not self._client:
            return []

        try:
            objects = await asyncio.to_thread(
                self._client.list_objects,
                self._bucket_exports,
                prefix=prefix,
                recursive=True,
            )

            exports = []
            for obj in objects:
                if len(exports) >= limit:
                    break
                exports.append({
                    "name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified,
                    "etag": obj.etag,
                })

            return exports

        except S3Error as e:
            self._logger.error(f"❌ List exports failed: {e}")
            return []

    # =========================================================================
    # Statistics
    # =========================================================================

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get MinIO storage statistics.

        Returns:
            Statistics dictionary
        """
        if not self._client:
            return {"error": "Not connected"}

        try:
            # Count objects in each bucket
            archive_count = 0
            document_count = 0
            export_count = 0

            for obj in await asyncio.to_thread(
                self._client.list_objects, self._bucket_archives, recursive=True
            ):
                archive_count += 1

            for obj in await asyncio.to_thread(
                self._client.list_objects, self._bucket_documents, recursive=True
            ):
                document_count += 1

            for obj in await asyncio.to_thread(
                self._client.list_objects, self._bucket_exports, recursive=True
            ):
                export_count += 1

            return {
                "connected": True,
                "endpoint": f"{self._config.get('endpoint')}:{self._config.get('port')}",
                "archives_count": archive_count,
                "documents_count": document_count,
                "exports_count": export_count,
                "buckets": {
                    "archives": self._bucket_archives,
                    "documents": self._bucket_documents,
                    "exports": self._bucket_exports,
                },
            }

        except S3Error as e:
            return {
                "connected": False,
                "error": str(e),
            }


# =============================================================================
# Factory Function
# =============================================================================


async def create_minio_manager(
    config_manager,
    secrets_manager,
    logging_manager,
) -> MinIOManager:
    """
    Factory function to create and connect MinIOManager.

    Following Clean Architecture v5.2 Rule #1: Factory Functions.

    Args:
        config_manager: ConfigManager instance
        secrets_manager: SecretsManager instance
        logging_manager: LoggingManager instance

    Returns:
        Connected MinIOManager instance

    Raises:
        ConnectionError: If MinIO connection fails
    """
    logger = logging_manager.get_logger("src.managers.archive.minio_manager")
    logger.info("🏭 Creating MinIOManager")

    # Get MinIO configuration
    minio_config = config_manager.get_minio_config()

    # Get MinIO credentials from secrets
    access_key = secrets_manager.get_minio_access_key()
    secret_key = secrets_manager.get_minio_secret_key()

    # Create manager
    manager = MinIOManager(
        config=minio_config,
        access_key=access_key,
        secret_key=secret_key,
        logging_manager=logging_manager,
    )

    # Connect
    await manager.connect()

    return manager


__all__ = [
    "MinIOManager",
    "create_minio_manager",
]
