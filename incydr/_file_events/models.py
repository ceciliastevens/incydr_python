from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from incydr._core.models import ResponseModel
from incydr.enums import Enum
from incydr.enums import SortDirection
from incydr.enums.file_events import EventSearchTerm
from incydr.enums.file_events import EventType
from incydr.enums.file_events import FileType
from incydr.enums.file_events import Operator
from incydr.enums.file_events import RemoteActivity
from incydr.enums.file_events import ReportType
from incydr.enums.file_events import RiskSeverity
from incydr.enums.file_events import SearchProblemType
from incydr.enums.file_events import Shared


class Model(BaseModel):
    __root__: Any


class GroupClause(Enum):
    """
    Grouping clause for any specified groups.  Default is `AND`.
    """

    and_ = "AND"
    or_ = "OR"


class DestinationEmail(BaseModel):
    recipients: Optional[List[str]] = Field(
        None,
        description="The email addresses of those who received the email. Includes the To, Cc, and Bcc recipients.",
        example=["cody@example.com", "theboss@example.com"],
    )
    subject: Optional[str] = Field(
        None,
        description="The subject of the email message.",
        example="Important business documents",
    )


class DestinationUser(BaseModel):
    email: Optional[List[str]] = Field(
        None,
        description="For endpoint events where a file in cloud storage is synced to a device, the email address of the user logged in to the cloud storage provider. For cloud events, the email addresses of users added as sharing recipients. In some case, OneDrive events may return multiple values, but this is often the same username formatted in different ways.",
        example=["first.last@example.com", "first_last_example_com"],
    )


class FieldError(BaseModel):
    error: Optional[str] = Field(
        None,
        description="Error indicating why the field could not be determined.",
        example="Hash unavailable. Locked file.",
    )
    field: Optional[str] = Field(
        None,
        description="FileEvent field that could not be determined.",
        example="md5Checksum",
    )


class FileClassification(BaseModel):
    value: Optional[str] = Field(
        None,
        description="The classification value applied to the file.",
        example="Classified",
    )
    vendor: Optional[str] = Field(
        None,
        description="The name of the vendor that classified the file.",
        example="MICROSOFT INFORMATION PROTECTION",
    )


class Group(BaseModel):
    doc_count: Optional[int] = Field(
        None,
        alias="docCount",
        description="The approximate count of hits matching this value for your query.",
        example=3,
    )
    value: Optional[str] = Field(
        None, description="The value of the term for this group.", example="readme.md"
    )


class Hash(BaseModel):
    md5: Optional[str] = Field(
        None,
        description="The MD5 hash of the file contents.",
        example="a162591e78eb2c816a28907d3ac020f9",
    )
    md5_error: Optional[str] = Field(
        None, alias="md5Error", description="Reason the MD5 hash is unavailable."
    )
    sha256: Optional[str] = Field(
        None,
        description="The SHA-256 hash of the file contents.",
        example="ded96d69c63754472efc4aa86fed68d4e17784b38089851cfa84e699e48b4155",
    )
    sha256_error: Optional[str] = Field(
        None, alias="sha256Error", description="Reason the SHA-256 hash is unavailable."
    )


class Process(BaseModel):
    executable: Optional[str] = Field(
        None,
        description="The name of the process that accessed the file, as reported by the device’s operating system. Depending on your Code42 product plan, this value may be null for some event types.",
        example="bash",
    )
    owner: Optional[str] = Field(
        None,
        description="The username of the process owner, as reported by the device’s operating system. Depending on your Code42 product plan, this value may be null for some event types.",
        example="root",
    )


class RemovableMedia(BaseModel):
    bus_type: Optional[str] = Field(
        None,
        alias="busType",
        description="For events detected on removable media, indicates the communication system used to transfer data between the host and the removable device.",
        example="USB 3.0 Bus",
    )
    capacity: Optional[int] = Field(
        None,
        description="For events detected on removable media, the capacity of the removable device in bytes.",
        example=15631122432,
    )
    media_name: Optional[str] = Field(
        None,
        alias="mediaName",
        description="For events detected on removable media, the media name of the device, as reported by the vendor/device. This is usually very similar to the productName, but can vary based on the rule_type of device. For example, if the device is a hard drive in a USB enclosure, this may be the combination of the drive model and the enclosure model.\nThis value is not provided by all devices, so it may be null in some cases.",
        example="Cruzer Blade",
    )
    name: Optional[str] = Field(
        None,
        description="For events detected on removable media, the name of the removable device.",
        example="JUMPDRIVE",
    )
    partition_id: Optional[List[str]] = Field(
        None,
        alias="partitionId",
        description="For events detected on removable media, a unique identifier assigned to the volume/partition when it was formatted. Windows devices refer to this as the VolumeGuid. On Mac devices, this is the Disk / Partition UUID, which appears when running the Terminal command diskUtil info.",
        example=["disk0s2", "disk0s3"],
    )
    serial_number: Optional[str] = Field(
        None,
        alias="serialNumber",
        description="For events detected on removable media, the serial number of the removable device.",
        example="4C531001550407108465",
    )
    vendor: Optional[str] = Field(
        None,
        description="For events detected on removable media, the vendor of the removable device.",
        example="SanDisk",
    )
    volume_name: Optional[List[str]] = Field(
        None,
        alias="volumeName",
        description='For events detected on removable media, the name assigned to the volume when it was formatted, as reported by the device\'s operating system. This is also frequently called the "partition" name.',
        example=["MY_FILES"],
    )


class Report(BaseModel):
    count: Optional[int] = Field(
        None, description="The total number of rows returned in the report.", example=20
    )
    description: Optional[str] = Field(
        None,
        description="The description of the report.",
        example="Top 20 accounts based on annual revenue",
    )
    headers: Optional[List[str]] = Field(
        None,
        description="The list of EventSearchTerm headers that are in the report.",
        example=[
            "USERNAME",
            "ACCOUNT_NAME",
            "TYPE",
            "DUE_DATE",
            "LAST_UPDATE",
            "ADDRESS1_STATE",
        ],
    )
    id: Optional[str] = Field(
        None,
        description="The ID of the report associated with this event.",
        example="00OB00000042FHdMAM",
    )
    name: Optional[str] = Field(
        None,
        description="The display name of the report.",
        example="Top Accounts Report",
    )
    type: Optional[ReportType] = Field(
        None,
        description='Indicates if the report is "REPORT_TYPE_AD_HOC" or "REPORT_TYPE_SAVED".',
        example="REPORT_TYPE_SAVED",
    )


class RiskIndicator(BaseModel):
    name: Optional[str] = Field(
        None, description="Name of the risk indicator.", example="Browser upload"
    )
    weight: Optional[int] = Field(
        None,
        description="Configured weight of the risk indicator at the time this event was seen.",
        example=5,
    )


class SearchFilterSearchTermV1(BaseModel):
    operator: Optional[Operator] = Field(
        None,
        description="The rule_type of match to perform.  Default value is `IS`.",
        example="IS_NOT",
    )
    term: Optional[EventSearchTerm] = Field(
        None, description="The field to match.", example="eventId"
    )
    value: str = Field(
        ..., description="The input for the search.", example="ari@example.com"
    )


class SearchFilterSearchTermV1Res(BaseModel):
    operator: Optional[Operator] = Field(
        None,
        description="The rule_type of match to perform.  Default value is `IS`.",
        example="IS_NOT",
    )
    term: Optional[EventSearchTerm] = Field(
        None, description="The field to match.", example="eventId"
    )
    value: str = Field(
        ..., description="The input for the search.", example="ari@example.com"
    )


class SearchFilterSearchTermV2(BaseModel):
    operator: Optional[Operator] = Field(
        None,
        description="The rule_type of match to perform.  Default value is `IS`.",
        example="IS_NOT",
    )
    term: Optional[EventSearchTerm] = Field(
        None, description="The field to match.", example="user.email"
    )
    value: str = Field(
        ..., description="The input for the search.", example="ari@example.com"
    )


class SearchFilterSearchTermV2Res(BaseModel):
    operator: Optional[Operator] = Field(
        None,
        description="The rule_type of match to perform.  Default value is `IS`.",
        example="IS_NOT",
    )
    term: Optional[EventSearchTerm] = Field(
        None, description="The field to match.", example="user.email"
    )
    value: str = Field(
        ..., description="The input for the search.", example="ari@example.com"
    )


class SharedWithUser(BaseModel):
    cloud_username: Optional[str] = Field(
        None,
        alias="cloudUsername",
        description="Name of the user reported by the cloud provider with whom the file was shared.",
        example="alix@example.com",
    )


class SourceEmail(BaseModel):
    from_: Optional[str] = Field(
        None,
        alias="from",
        description='The display name of the sender, as it appears in the "From" field in the email. In many cases, this is the same as source.email.sender, but it can be different if the message is sent by a server or other mail agent on behalf of someone else.',
        example="ari@example.com",
    )
    sender: Optional[str] = Field(
        None,
        description="The address of the entity responsible for transmitting the message. In many cases, this is the same as source.email.from, but it can be different if the message is sent by a server or other mail agent on behalf of someone else.",
        example="ari@example.com",
    )


class StreamingResponseBody(BaseModel):
    pass


class Tab(BaseModel):
    title: Optional[str] = Field(
        None,
        description="The title of this app or browser tab.",
        example="Example Domain",
    )
    title_error: Optional[str] = Field(
        None,
        alias="titleError",
        description="Reason the title of this app or browser tab is unavailable.",
        example="InsufficientPermissions",
    )
    url: Optional[str] = Field(
        None, description="The URL of this browser tab.", example="https://example.com/"
    )
    url_error: Optional[str] = Field(
        None,
        alias="urlError",
        description="Reason the URL of this browser tab is unavailable.",
        example="InsufficientPermissions",
    )


class User(BaseModel):
    device_uid: Optional[str] = Field(
        None,
        alias="deviceUid",
        description="Unique identifier for the device. Null if the file event occurred on a cloud provider.",
        example=24681,
    )
    email: Optional[str] = Field(
        None,
        description="The Code42 username used to sign in to the Code42 app on the device. Null if the file event occurred on a cloud provider.",
        example="cody@example.com",
    )
    id: Optional[str] = Field(
        None,
        description="Unique identifier for the user of the Code42 app on the device. Null if the file event occurred on a cloud provider.",
        example=1138,
    )


class Destination(BaseModel):
    account_name: Optional[str] = Field(
        None,
        alias="accountName",
        description="For cloud sync apps installed on user devices, the name of the cloud account where the event was observed. This can help identify if the activity occurred in a business or personal account.",
    )
    account_type: Optional[str] = Field(
        None,
        alias="accountType",
        description="For cloud sync apps installed on user devices, the rule_type of account where the event was observed. For example, 'BUSINESS' or 'PERSONAL'.",
        example="BUSINESS",
    )
    category: Optional[str] = Field(
        None,
        description="General category of where the file originated. For example: Cloud Storage, Email, Social Media.",
        example="Social Media",
    )
    domains: Optional[List[str]] = Field(
        None,
        description="The domain section of the URLs reported in destination.tabs.url.",
    )
    email: Optional[DestinationEmail] = Field(
        None, description="Metadata about the destination email."
    )
    ip: Optional[str] = Field(
        None,
        description="The external IP address of the user's device.",
        example="127.0.0.1",
    )
    name: Optional[str] = Field(
        None,
        description="The name reported by the device's operating system.  This may be different than the device name in the Code42 console.",
        example="Mari's MacBook",
    )
    operating_system: Optional[str] = Field(
        None,
        alias="operatingSystem",
        description="The operating system of the destination device.",
        example="Windows 10",
    )
    print_job_name: Optional[str] = Field(
        None,
        alias="printJobName",
        description="For print events, the name of the print job, as reported by the user's device.",
        example="printer.exe",
    )
    printer_name: Optional[str] = Field(
        None,
        alias="printerName",
        description="For print events, the name of the printer the job was sent to.",
        example="OfficeJet",
    )
    private_ip: List[str] = Field(
        ...,
        alias="privateIp",
        description="The IP address of the user's device on your internal network, including Network interfaces, Virtual Network Interface controllers (NICs), and Loopback/non-routable addresses.",
        example=["127.0.0.1", "127.0.0.2"],
    )
    removable_media: Optional[RemovableMedia] = Field(
        None,
        alias="removableMedia",
        description="Metadata about the removable media destination.",
    )
    tabs: Optional[List[Tab]] = Field(
        None, description="Metadata about the browser tab destination."
    )
    user: Optional[DestinationUser] = Field(
        None, description="Metadata about the destination user."
    )


class File(BaseModel):
    category: Optional[str] = Field(
        None,
        description="A categorization of the file that is inferred from MIME rule_type.",
        example="Audio",
    )
    category_by_bytes: Optional[str] = Field(
        None,
        alias="categoryByBytes",
        description="A categorization of the file based on its contents.",
        example="Image",
    )
    category_by_extension: Optional[str] = Field(
        None,
        alias="categoryByExtension",
        description="A categorization of the file based on its extension.",
        example="Document",
    )
    classifications: Optional[List[FileClassification]] = Field(
        None, description="Data provided by an external file classification vendor."
    )
    cloud_drive_id: Optional[str] = Field(
        None,
        alias="cloudDriveId",
        description="Unique identifier reported by the cloud provider for the drive containing the file at the time the event occurred.",
        example="RvBpZ48u2m",
    )
    created: Optional[datetime] = Field(
        None,
        description="File creation timestamp as reported by the device's operating system in Coordinated Universal Time (UTC); available for Mac and Windows NTFS devices only.",
        example="2020-10-27T15:16:05.369203Z",
    )
    directory: Optional[str] = Field(
        None,
        description="The file location on the user's device; a forward or backslash must be included at the end of the filepath. Possibly null if the file event occurred on a cloud provider.",
        example="/Users/alix/Documents/",
    )
    directory_id: Optional[List[str]] = Field(
        None,
        alias="directoryId",
        description="Unique identifiers of the parent drives that contain the file; searching on directoryId will return events for all of the files contained in the parent drive.",
        example=["1234", "56d78"],
    )
    hash: Optional[Hash] = Field(None, description="Hash values of the file.")
    id: Optional[str] = Field(
        None,
        description="Unique identifier reported by the cloud provider for the file associated with the event.",
        example="PUL5zWLRrdudiJZ1OCWw",
    )
    mime_type_by_bytes: Optional[str] = Field(
        None,
        alias="mimeTypeByBytes",
        description="The MIME rule_type of the file based on its contents.",
        example="text/csv",
    )
    mime_type_by_extension: Optional[str] = Field(
        None,
        alias="mimeTypeByExtension",
        description="The MIME rule_type of the file based on its extension.",
        example="audio/vorbis",
    )
    modified: Optional[datetime] = Field(
        None,
        description="File modification timestamp as reported by the device's operating system.  This only indicates changes to file contents.  Changes to file permissions, file owner, or other metadata are not reflected in this timestamp.  Date is reported in Coordinated Universal Time (UTC).",
        example="2020-10-27T15:16:05.369203Z",
    )
    name: str = Field(
        ...,
        description="The name of the file, including the file extension.",
        example="ReadMe.md",
    )
    owner: Optional[str] = Field(
        None,
        description="The name of the user who owns the file as reported by the device's file system.",
        example="ari.example",
    )
    size_in_bytes: Optional[int] = Field(
        None, alias="sizeInBytes", description="Size of the file in bytes.", example=256
    )
    url: Optional[str] = Field(
        None,
        description="URL reported by the cloud provider at the time the event occurred.",
        example="https://example.com",
    )


class FileEventV1(BaseModel):
    actor: Optional[str] = Field(
        None,
        description="Name of the user reported by the cloud provider for the user who performed this file activity.",
        example="casey@example.com",
    )
    cloud_drive_id: Optional[str] = Field(
        None,
        alias="cloudDriveId",
        description="Unique identifier reported by the cloud provider for the drive containing the file at the time the event occurred.",
        example="RvBpZ48u2m",
    )
    create_timestamp: Optional[datetime] = Field(
        None,
        alias="createTimestamp",
        description="File creation timestamp as reported by the device's operating system in Coordinated Universal Time (UTC); available for Mac and Windows NTFS devices only.",
        example="2020-10-27T15:16:05.369203Z",
    )
    destination_category: Optional[str] = Field(
        None,
        alias="destinationCategory",
        description="General category of where the file was sent. For example: Cloud Storage, Email, Social Media.",
        example="Social Media",
    )
    destination_name: Optional[str] = Field(
        None,
        alias="destinationName",
        description="Specific target of where the file was sent. For example: Google Drive, Outlook, Slack.",
        example="LinkedIn",
    )
    detection_source_alias: Optional[str] = Field(
        None,
        alias="detectionSourceAlias",
        description="Name provided by a Code42 Customer Cloud Administrator when a Cloud Connector is initially configured.",
        example="R&D OneDrive",
    )
    device_uid: Optional[str] = Field(
        None,
        alias="deviceUid",
        description="Unique identifier for the device. Null if the file event occurred on a cloud provider.",
        example=24681,
    )
    device_user_name: Optional[str] = Field(
        None,
        alias="deviceUserName",
        description="The Code42 username used to sign in to the Code42 app on the device. Null if the file event occurred on a cloud provider.",
        example="cody@example.com",
    )
    directory_id: Optional[List[str]] = Field(
        None,
        alias="directoryId",
        description="Unique identifiers of the parent drives that contain the file; searching on directoryId will return events for all of the files contained in the parent drive.",
        example=["1234", "56d78"],
    )
    domain_name: Optional[str] = Field(
        None,
        alias="domainName",
        description="Fully qualified domain name (FQDN) for the user's device at the time the event is recorded.  If the device is unable to resolve the domain name of the host, it reports the IP address of the host.",
        example="localhost",
    )
    email_dlp_policy_names: Optional[List[str]] = Field(
        None,
        alias="emailDlpPolicyNames",
        description="No longer in use. Deprecated September 2021.",
        example=["External recipient"],
    )
    email_from: Optional[str] = Field(
        None,
        alias="emailFrom",
        description='The display name of the sender, as it appears in the "From" field in the email. In many cases, this is the same as emailSender, but it can be different if the message is sent by a server or other mail agent on behalf of someone else.',
        example="ari@example.com",
    )
    email_recipients: Optional[List[str]] = Field(
        None,
        alias="emailRecipients",
        description=" The email addresses of those who received the email. Includes the To, Cc, and Bcc recipients.",
        example=["cody@example.com", "theboss@example.com"],
    )
    email_sender: Optional[str] = Field(
        None,
        alias="emailSender",
        description="The address of the entity responsible for transmitting the message. In many cases, this is the same as emailFrom, but it can be different if the message is sent by a server or other mail agent on behalf of someone else.",
        example="ari@example.com",
    )
    email_subject: Optional[str] = Field(
        None,
        alias="emailSubject",
        description="The subject of the email message.",
        example="Important business documents",
    )
    event_id: str = Field(
        ...,
        alias="eventId",
        description="The unique identifier for the event.",
        example="0_147e9445-2f30-4a91-8b2a-9455332e880a_973435567569502913_986467523038446097_163",
    )
    event_timestamp: Optional[datetime] = Field(
        None,
        alias="eventTimestamp",
        description="Date and time that the Code42 service on the device detected an event; based on the device’s system clock and reported in Coordinated Universal Time (UTC).",
        example="2020-10-27T15:16:05.369203Z",
    )
    event_type: EventType = Field(
        ...,
        alias="eventType",
        description="Indicates the rule_type of file event observed.",
        example="MODIFIED",
    )
    exposure: List[str] = Field(
        ...,
        description="Lists indicators that the data may be exposed. Default is `[]`.",
        example=["CloudStorage"],
    )
    field_errors: Optional[List[FieldError]] = Field(
        None,
        alias="fieldErrors",
        description="List fields with errors indicating why they could not be determined.",
        example=[{"field": "md5Checksum", "error": "Hash unavailable. Locked file."}],
    )
    file_category: Optional[str] = Field(
        None,
        alias="fileCategory",
        description="A categorization of the file that is inferred from MIME rule_type.",
        example="Audio",
    )
    file_category_by_bytes: Optional[str] = Field(
        None,
        alias="fileCategoryByBytes",
        description="A categorization of the file based on its contents.",
        example="Image",
    )
    file_category_by_extension: Optional[str] = Field(
        None,
        alias="fileCategoryByExtension",
        description="A categorization of the file based on its extension.",
        example="Document",
    )
    file_classifications: Optional[List[FileClassification]] = Field(
        None,
        alias="fileClassifications",
        description="Data provided by an external file classification vendor.",
    )
    file_id: Optional[str] = Field(
        None,
        alias="fileId",
        description="Unique identifier reported by the cloud provider for the file associated with the event.",
        example="PUL5zWLRrdudiJZ1OCWw",
    )
    file_name: str = Field(
        ...,
        alias="fileName",
        description="The name of the file, including the file extension.",
        example="ReadMe.md",
    )
    file_owner: Optional[str] = Field(
        None,
        alias="fileOwner",
        description="The name of the user who owns the file as reported by the device's file system.",
        example="ari.example",
    )
    file_path: Optional[str] = Field(
        None,
        alias="filePath",
        description="The file location on the user's device; a forward or backslash must be included at the end of the filepath. Possibly null if the file event occurred on a cloud provider.",
        example="/Users/alix/Documents/",
    )
    file_size: Optional[int] = Field(
        None, alias="fileSize", description="Size of the file in bytes.", example=256
    )
    file_type: FileType = Field(
        ...,
        alias="fileType",
        description="The rule_type of file detected; only FILE types are searchable.",
        example="FILE",
    )
    insertion_timestamp: Optional[datetime] = Field(
        None,
        alias="insertionTimestamp",
        description="Date and time that the event was received for indexing by Code42; timestamp is based on the Code42 server system clock and reported in Coordinated Universal Time (UTC).",
        example="2020-10-27T15:16:05.369203Z",
    )
    md5_checksum: Optional[str] = Field(
        None,
        alias="md5Checksum",
        description="The MD5 hash of the file contents.",
        example="a162591e78eb2c816a28907d3ac020f9",
    )
    mime_type_by_bytes: Optional[str] = Field(
        None,
        alias="mimeTypeByBytes",
        description="The MIME rule_type of the file based on its contents.",
        example="text/csv",
    )
    mime_type_by_extension: Optional[str] = Field(
        None,
        alias="mimeTypeByExtension",
        description="The MIME rule_type of the file based on its extension.",
        example="audio/vorbis",
    )
    mime_type_mismatch: Optional[bool] = Field(
        None,
        alias="mimeTypeMismatch",
        description="Indicates whether or not the MIME rule_type of the file based on its contents does not match the MIME rule_type based on its extension and that this mismatch is unexpected.",
        example=True,
    )
    modify_timestamp: Optional[datetime] = Field(
        None,
        alias="modifyTimestamp",
        description="File modification timestamp as reported by the device's operating system.  This only indicates changes to file contents.  Changes to file permissions, file owner, or other metadata are not reflected in this timestamp.  Date is reported in Coordinated Universal Time (UTC).",
        example="2020-10-27T15:16:05.369203Z",
    )
    operating_system_user: Optional[str] = Field(
        None,
        alias="operatingSystemUser",
        description="The username logged in to the device when the file activity was observed, as reported by the device’s operating system.",
        example="ari.example",
    )
    os_host_name: Optional[str] = Field(
        None,
        alias="osHostName",
        description="The name reported by the device's operating system.  This may be different than the device name in the Code42 console.",
        example="Mari's MacBook",
    )
    outside_active_hours: Optional[bool] = Field(
        None,
        alias="outsideActiveHours",
        description="Indicates whether or not this event occurred outside of the user's typical active hours using data modeling from the this user's prior activity.",
        example=False,
    )
    print_job_name: Optional[str] = Field(
        None,
        alias="printJobName",
        description="For print events, the name of the print job, as reported by the user's device.",
        example="printer.exe",
    )
    printer_name: Optional[str] = Field(
        None,
        alias="printerName",
        description="For print events, the name of the printer the job was sent to.",
        example="OfficeJet",
    )
    private_ip_addresses: List[str] = Field(
        ...,
        alias="privateIpAddresses",
        description="The IP address of the user's device on your internal network, including Network interfaces, Virtual Network Interface controllers (NICs), and Loopback/non-routable addresses.",
        example=["127.0.0.1", "127.0.0.2"],
    )
    process_name: Optional[str] = Field(
        None,
        alias="processName",
        description="The name of the process that accessed the file, as reported by the device’s operating system. Depending on your Code42 product plan, this value may be null for some event types.",
        example="bash",
    )
    process_owner: Optional[str] = Field(
        None,
        alias="processOwner",
        description="The username of the process owner, as reported by the device’s operating system. Depending on your Code42 product plan, this value may be null for some event types.",
        example="root",
    )
    public_ip_address: Optional[str] = Field(
        None,
        alias="publicIpAddress",
        description="The external IP address of the user's device.",
        example="127.0.0.1",
    )
    remote_activity: Optional[RemoteActivity] = Field(
        None,
        alias="remoteActivity",
        description='For endpoint events, compares the IP address of the file event to your defined list of addresses in the Data Preferences section of the Code42 console. If the IP address from the file event does not match, "remote" is true. If the IP address does match, "remote" is false.',
        example="UNKNOWN",
    )
    removable_media_bus_type: Optional[str] = Field(
        None,
        alias="removableMediaBusType",
        description="For events detected on removable media, indicates the communication system used to transfer data between the host and the removable device.",
        example="USB 3.0 Bus",
    )
    removable_media_capacity: Optional[int] = Field(
        None,
        alias="removableMediaCapacity",
        description="For events detected on removable media, the capacity of the removable device in bytes.",
        example=15631122432,
    )
    removable_media_media_name: Optional[str] = Field(
        None,
        alias="removableMediaMediaName",
        description="For events detected on removable media, the media name of the device, as reported by the vendor/device. This is usually very similar to the productName, but can vary based on the rule_type of device. For example, if the device is a hard drive in a USB enclosure, this may be the combination of the drive model and the enclosure model.\nThis value is not provided by all devices, so it may be null in some cases.",
        example="Cruzer Blade",
    )
    removable_media_name: Optional[str] = Field(
        None,
        alias="removableMediaName",
        description="For events detected on removable media, the name of the removable device.",
        example="JUMPDRIVE",
    )
    removable_media_partition_id: Optional[List[str]] = Field(
        None,
        alias="removableMediaPartitionId",
        description="For events detected on removable media, a unique identifier assigned to the volume/partition when it was formatted. Windows devices refer to this as the VolumeGuid. On Mac devices, this is the Disk / Partition UUID, which appears when running the Terminal command diskUtil info.",
        example=["disk0s2", "disk0s3"],
    )
    removable_media_serial_number: Optional[str] = Field(
        None,
        alias="removableMediaSerialNumber",
        description="For events detected on removable media, the serial number of the removable device.",
        example="4C531001550407108465",
    )
    removable_media_vendor: Optional[str] = Field(
        None,
        alias="removableMediaVendor",
        description="For events detected on removable media, the vendor of the removable device.",
        example="SanDisk",
    )
    removable_media_volume_name: Optional[List[str]] = Field(
        None,
        alias="removableMediaVolumeName",
        description='For events detected on removable media, the name assigned to the volume when it was formatted, as reported by the device\'s operating system. This is also frequently called the "partition" name.',
        example=["MY_FILES"],
    )
    report_EventSearchTerm_headers: Optional[List[str]] = Field(
        None,
        alias="reportEventSearchTermHeaders",
        description="The list of EventSearchTerm headers that are in the report.",
        example=[
            "USERNAME",
            "ACCOUNT_NAME",
            "TYPE",
            "DUE_DATE",
            "LAST_UPDATE",
            "ADDRESS1_STATE",
        ],
    )
    report_description: Optional[str] = Field(
        None,
        alias="reportDescription",
        description="The description of the report.",
        example="Top 20 accounts based on annual revenue",
    )
    report_id: Optional[str] = Field(
        None,
        alias="reportId",
        description="The ID of the report associated with this event.",
        example="00OB00000042FHdMAM",
    )
    report_name: Optional[str] = Field(
        None,
        alias="reportName",
        description="The display name of the report.",
        example="Top Accounts Report",
    )
    report_record_count: Optional[int] = Field(
        None,
        alias="reportRecordCount",
        description="The total number of rows returned in the report.",
        example=20,
    )
    report_type: Optional[ReportType] = Field(
        None,
        alias="reportType",
        description='Indicates if the report is "REPORT_TYPE_AD_HOC" or "REPORT_TYPE_SAVED".',
        example="REPORT_TYPE_SAVED",
    )
    risk_indicators: Optional[List[RiskIndicator]] = Field(
        None,
        alias="riskIndicators",
        description="List of risk indicators identified for this event. If more than one risk indicator applies to this event, the sum of all indicators determines the total risk score.",
    )
    risk_score: Optional[int] = Field(
        None,
        alias="riskScore",
        description="Sum of the weights for each risk indicator. This score is used to determine the overall risk severity of the event.",
        example=12,
    )
    risk_severity: Optional[RiskSeverity] = Field(
        None,
        alias="riskSeverity",
        description="The general risk assessment of the event, based on the numeric score.",
        example="CRITICAL",
    )
    sha256_checksum: Optional[str] = Field(
        None,
        alias="sha256Checksum",
        description="The SHA256 hash of the file contents.",
        example="ded96d69c63754472efc4aa86fed68d4e17784b38089851cfa84e699e48b4155",
    )
    shared: Optional[Shared] = Field(
        None,
        description="Indicates the shared status as reported by the cloud provider at the time the event occurred. A shared file indicates that one or more users have been granted explicit access to the file. It does not capture whether or not a link to the file has been shared.",
        example="TRUE",
    )
    shared_with: Optional[SharedWithUser] = Field(
        None,
        alias="sharedWith",
        description="A list of users who have been granted explicit rights to the file at the time the event occurred.",
        example=[{"cloudUsername": "alix@example.com"}],
    )
    sharing_type_added: Optional[List[str]] = Field(
        None,
        alias="sharingTypeAdded",
        description="Public sharing types that were added by this event.",
        example=["SharedViaLink"],
    )
    source: Optional[str] = Field(
        None, description="Data source for a file event.", example="OneDrive"
    )
    source_category: Optional[str] = Field(
        None,
        alias="sourceCategory",
        description="General category of where the file originated. For example: Cloud Storage, Email, Social Media.",
        example="Social Media",
    )
    source_name: Optional[str] = Field(
        None,
        alias="sourceName",
        description="Specific target of where the file originated. For example: Google Drive, Outlook, Slack.",
        example="Salesforce",
    )
    source_tabs: Optional[List[Tab]] = Field(
        None,
        alias="sourceTabs",
        description="For events generated when a file is downloaded via a browser or other app, the tabs that had activity at the time of the event.",
    )
    sync_destination: Optional[str] = Field(
        None,
        alias="syncDestination",
        description="For events detected within a cloud storage sync destination on a device, the name of the cloud storage vendor.",
        example="Dropbox",
    )
    sync_destination_username: Optional[List[str]] = Field(
        None,
        alias="syncDestinationUsername",
        description="For events detected within a cloud storage sync destination on a device, lists the usernames logged into the cloud storage provider when the file activity was observed.",
        example=["ari@example.com"],
    )
    tab_url: Optional[str] = Field(
        None,
        alias="tabUrl",
        description="For events generated when a file is read in a browser or other app, the URL that had activity at the time of the event. May not contain all URLs if multiple are present. 'tabs' field is recommended for use instead.",
        example="https://example.com",
    )
    tabs: Optional[List[Tab]] = Field(
        None,
        description="For events generated when a file is uploaded via a browser or other app, the tabs that had activity at the time of the event.",
    )
    trust_reason: Optional[str] = Field(
        None,
        alias="trustReason",
        description="The reason the event is trusted. trustReason is only populated if trusted is true for this event.",
        example="TRUSTED_DOMAIN_BROWSER_URL",
    )
    trusted: Optional[bool] = Field(
        None,
        description="Indicates whether or not the file activity is trusted based on your Data Preferences settings.",
        example=True,
    )
    url: Optional[str] = Field(
        None,
        description="URL reported by the cloud provider at the time the event occurred.",
        example="https://example.com",
    )
    user_uid: Optional[str] = Field(
        None,
        alias="userUid",
        description="Unique identifier for the user of the Code42 app on the device. Null if the file event occurred on a cloud provider.",
        example=1138,
    )
    window_title: Optional[List[str]] = Field(
        None,
        alias="windowTitle",
        description="For events generated when a file is read in a browser or other app, the tab or window title(s) that had activity at the time of the event. 'tabs' field is recommended for use instead.",
        example=["Inbox - cody@example.com"],
    )


class FilterGroupSearchTermV1(BaseModel):
    filter_clause: Optional[GroupClause] = Field(
        None,
        alias="filterClause",
        description="Grouping clause for filters.  Default is `AND`.",
        example="AND",
    )
    filters: List[SearchFilterSearchTermV1] = Field(
        ..., description="One or more SearchFilters to be combined in a query."
    )


class FilterGroupSearchTermV2(BaseModel):
    filter_clause: Optional[GroupClause] = Field(
        None,
        alias="filterClause",
        description="Grouping clause for filters.  Default is `AND`.",
        example="AND",
    )
    filters: List[SearchFilterSearchTermV2] = Field(
        ..., description="One or more SearchFilters to be combined in a query."
    )


class GroupingRequestSearchTermV1(BaseModel):
    group_clause: Optional[GroupClause] = Field(
        None,
        alias="groupClause",
        description="Grouping clause for any specified groups.  Default is `AND`.",
        example="AND",
    )
    grouping_term: Optional[EventSearchTerm] = Field(
        None,
        alias="groupingTerm",
        description="The search term to use to form the groups.",
        example="eventId",
    )
    groups: List[FilterGroupSearchTermV1] = Field(
        ..., description="One or more FilterGroups to be combined in a query."
    )


class GroupingRequestSearchTermV2(BaseModel):
    group_clause: Optional[GroupClause] = Field(
        None,
        alias="groupClause",
        description="Grouping clause for any specified groups.  Default is `AND`.",
        example="AND",
    )
    grouping_term: Optional[EventSearchTerm] = Field(
        None,
        alias="groupingTerm",
        description="The search term to use to form the groups.",
        example="event.action",
    )
    groups: List[FilterGroupSearchTermV2] = Field(
        ..., description="One or more FilterGroups to be combined in a query."
    )


class QueryProblemSearchTermV1(BaseModel):
    bad_filter: Optional[SearchFilterSearchTermV1Res] = Field(
        None,
        alias="badFilter",
        description="The search filter that caused this problem.",
    )
    description: Optional[str] = Field(
        None,
        description="Additional description of the problem.",
        example="Request timed out.  Refine your filter criteria and try again.",
    )
    type: SearchProblemType = Field(
        ...,
        description="The rule_type of problem that occured.",
        example="SEARCH_FAILED",
    )


class QueryProblemSearchTermV2(BaseModel):
    bad_filter: Optional[SearchFilterSearchTermV2Res] = Field(
        None,
        alias="badFilter",
        description="The search filter that caused this problem.",
    )
    description: Optional[str] = Field(
        None,
        description="Additional description of the problem.",
        example="Request timed out.  Refine your filter criteria and try again.",
    )
    type: SearchProblemType = Field(
        ...,
        description="The rule_type of problem that occured.",
        example="SEARCH_FAILED",
    )


class RelatedEvent(BaseModel):
    agent_timestamp: Optional[datetime] = Field(
        None,
        alias="agentTimestamp",
        description="Date and time that the Code42 service on the device detected an event; based on the device’s system clock and reported in Coordinated Universal Time (UTC).",
        example="2020-10-27T15:16:05.369203Z",
    )
    event_action: Optional[str] = Field(
        None,
        alias="eventAction",
        description="The rule_type of file event observed. For example: file-modified, application-read, removable-media-created.",
        example="file-downloaded",
    )
    id: Optional[str] = Field(
        None,
        description="The unique identifier for the event.",
        example="0_147e9445-2f30-4a91-8b2a-9455332e880a_973435567569502913_986467523038446097_163",
    )
    source_category: Optional[str] = Field(
        None,
        alias="sourceCategory",
        description="General category of where the file originated. For example: Cloud Storage, Email, Social Media.",
        example="Social Media",
    )
    source_name: Optional[str] = Field(
        None,
        alias="sourceName",
        description="The name reported by the device's operating system.  This may be different than the device name in the Code42 console.",
        example="Mari's MacBook",
    )
    tabs: Optional[List[Tab]] = Field(
        None, description="Metadata about the browser tab source."
    )
    user_email: Optional[str] = Field(
        None,
        alias="userEmail",
        description="The Code42 username used to sign in to the Code42 app on the device (for endpoint events) or the cloud service username of the person who caused the event (for cloud events).",
        example="cody@example.com",
    )


class Risk(BaseModel):
    indicators: Optional[List[RiskIndicator]] = Field(
        None,
        description="List of risk indicators identified for this event. If more than one risk indicator applies to this event, the sum of all indicators determines the total risk score.",
    )
    score: Optional[int] = Field(
        None,
        description="Sum of the weights for each risk indicator. This score is used to determine the overall risk severity of the event.",
        example=12,
    )
    severity: Optional[RiskSeverity] = Field(
        None,
        description="The general risk assessment of the event, based on the numeric score.",
        example="CRITICAL",
    )
    trust_reason: Optional[str] = Field(
        None,
        alias="trustReason",
        description="The reason the event is trusted. trustReason is only populated if trusted is true for this event.",
        example="TRUSTED_DOMAIN_BROWSER_URL",
    )
    trusted: Optional[bool] = Field(
        None,
        description="Indicates whether or not the file activity is trusted based on your Data Preferences settings.",
        example=True,
    )


class SavedSearchDetailSearchTermV1(BaseModel):
    api_version: Optional[int] = Field(
        None,
        alias="apiVersion",
        description="Version of the API used to create the search.",
        example=1,
    )
    EventSearchTerms: Optional[List[EventSearchTerm]] = Field(
        None,
        description="List of EventSearchTerms to be displayed in the web app for the search.",
    )
    created_by_uid: Optional[str] = Field(
        None,
        alias="createdByUID",
        description="User UID of the user who created the saved search.",
        example=806150685834341101,
    )
    created_by_username: Optional[str] = Field(
        None,
        alias="createdByUsername",
        description="Username of the user who created the saved search.",
        example="adrian@example.com",
    )
    creation_timestamp: Optional[datetime] = Field(
        None,
        alias="creationTimestamp",
        description="Time at which the saved search was created.",
        example="2020-10-27T15:16:05.369203Z",
    )
    group_clause: Optional[GroupClause] = Field(
        None,
        alias="groupClause",
        description="Grouping clause for any specified groups.",
        example="OR",
    )
    groups: Optional[List[FilterGroupSearchTermV1]] = Field(
        None, description="One or more FilterGroups to be combined in a query."
    )
    id: Optional[str] = Field(
        None,
        description="Unique identifier for the saved search.",
        example="cde979fa-d551-4be9-b242-39e75b824089",
    )
    modified_by_uid: Optional[str] = Field(
        None,
        alias="modifiedByUID",
        description="User UID of the user who last modified the saved search.",
        example=421380797518239242,
    )
    modified_by_username: Optional[str] = Field(
        None,
        alias="modifiedByUsername",
        description="Username of the user who last modified the saved search.",
        example="ari@example.com",
    )
    modified_timestamp: Optional[datetime] = Field(
        None,
        alias="modifiedTimestamp",
        description="Time at which the saved search was last modified.",
        example="2020-10-27T15:20:26.311894Z",
    )
    name: Optional[str] = Field(
        None,
        description="Name given to the saved search.",
        example="Example saved search",
    )
    notes: Optional[str] = Field(
        None,
        description="Optional notes about the search.",
        example="This search returns all events.",
    )
    srt_dir: Optional[SortDirection] = Field(
        None, alias="srtDir", description="Sort direction.", example="asc"
    )
    srt_key: Optional[EventSearchTerm] = Field(
        None, alias="srtKey", description="Search term for sorting.", example="eventId"
    )


class SavedSearchDetailSearchTermV2(BaseModel):
    api_version: Optional[int] = Field(
        None,
        alias="apiVersion",
        description="Version of the API used to create the search.",
        example=1,
    )
    EventSearchTerms: Optional[List[EventSearchTerm]] = Field(
        None,
        description="List of EventSearchTerms to be displayed in the web app for the search.",
    )
    created_by_uid: Optional[str] = Field(
        None,
        alias="createdByUID",
        description="User UID of the user who created the saved search.",
        example=806150685834341101,
    )
    created_by_username: Optional[str] = Field(
        None,
        alias="createdByUsername",
        description="Username of the user who created the saved search.",
        example="adrian@example.com",
    )
    creation_timestamp: Optional[datetime] = Field(
        None,
        alias="creationTimestamp",
        description="Time at which the saved search was created.",
        example="2020-10-27T15:16:05.369203Z",
    )
    group_clause: Optional[GroupClause] = Field(
        None,
        alias="groupClause",
        description="Grouping clause for any specified groups.",
        example="OR",
    )
    groups: Optional[List[FilterGroupSearchTermV2]] = Field(
        None, description="One or more FilterGroups to be combined in a query."
    )
    id: Optional[str] = Field(
        None,
        description="Unique identifier for the saved search.",
        example="cde979fa-d551-4be9-b242-39e75b824089",
    )
    modified_by_uid: Optional[str] = Field(
        None,
        alias="modifiedByUID",
        description="User UID of the user who last modified the saved search.",
        example=421380797518239242,
    )
    modified_by_username: Optional[str] = Field(
        None,
        alias="modifiedByUsername",
        description="Username of the user who last modified the saved search.",
        example="ari@example.com",
    )
    modified_timestamp: Optional[datetime] = Field(
        None,
        alias="modifiedTimestamp",
        description="Time at which the saved search was last modified.",
        example="2020-10-27T15:20:26.311894Z",
    )
    name: Optional[str] = Field(
        None,
        description="Name given to the saved search.",
        example="Example saved search",
    )
    notes: Optional[str] = Field(
        None,
        description="Optional notes about the search.",
        example="This search returns all events.",
    )
    srt_dir: Optional[SortDirection] = Field(
        None, alias="srtDir", description="Sort direction.", example="asc"
    )
    srt_key: Optional[EventSearchTerm] = Field(
        None, alias="srtKey", description="Search term for sorting.", example="eventId"
    )


class SavedSearchResponseSearchTermV1(BaseModel):
    searches: Optional[List[SavedSearchDetailSearchTermV1]] = Field(
        None, description="List of saved searches in the response."
    )


class SavedSearchResponseSearchTermV2(BaseModel):
    searches: Optional[List[SavedSearchDetailSearchTermV2]] = Field(
        None, description="List of saved searches in the response."
    )


class SearchRequestSearchTermV1(BaseModel):
    group_clause: Optional[GroupClause] = Field(
        None,
        alias="groupClause",
        description="Grouping clause for any specified groups.  Default is `AND`.",
        example="OR",
    )
    groups: List[FilterGroupSearchTermV1] = Field(
        ..., description="One or more FilterGroups to be combined in a query."
    )
    pg_num: Optional[int] = Field(
        None,
        alias="pgNum",
        description="Page number for search; ignored if pgToken is included.  Default is 1.",
        example=1,
    )
    pg_size: Optional[int] = Field(
        None,
        alias="pgSize",
        description="Max number of results to return for a page.  Default is 100.",
        example=100,
    )
    pg_token: Optional[str] = Field(
        None,
        alias="pgToken",
        description="A token used to indicate the starting point for additional page results. Typically, you obtain the pgToken value from the nextPgToken provided in a previous request. A pgToken is the only way to page past 10,000 results. If pgToken is supplied, pgNum is ignored. Provide empty string to retrieve the 'first page of results and null to use the pgNum value.  Default is null.",
        example="0_147e9445-2f30-4a91-8b2a-9455332e880a_973435567569502913_986467523038446097_163",
    )
    srt_dir: Optional[SortDirection] = Field(
        None,
        alias="srtDir",
        description="Sort direction.  Default is `desc`.",
        example="asc",
    )
    srt_key: Optional[EventSearchTerm] = Field(
        None, alias="srtKey", description="Search term for sorting.", example="eventId"
    )


class SearchRequestSearchTermV2(BaseModel):
    group_clause: Optional[GroupClause] = Field(
        None,
        alias="groupClause",
        description="Grouping clause for any specified groups.  Default is `AND`.",
        example="OR",
    )
    groups: List[FilterGroupSearchTermV2] = Field(
        ..., description="One or more FilterGroups to be combined in a query."
    )
    pg_num: Optional[int] = Field(
        None,
        alias="pgNum",
        description="Page number for search; ignored if pgToken is included.  Default is 1.",
        example=1,
    )
    pg_size: Optional[int] = Field(
        None,
        alias="pgSize",
        description="Max number of results to return for a page.  Default is 100.",
        example=100,
    )
    pg_token: Optional[str] = Field(
        None,
        alias="pgToken",
        description="A token used to indicate the starting point for additional page results. Typically, you obtain the pgToken value from the nextPgToken provided in a previous request. A pgToken is the only way to page past 10,000 results. If pgToken is supplied, pgNum is ignored. Provide empty string to retrieve the 'first page of results and null to use the pgNum value.  Default is null.",
        example="0_147e9445-2f30-4a91-8b2a-9455332e880a_973435567569502913_986467523038446097_163",
    )
    srt_dir: Optional[SortDirection] = Field(
        None,
        alias="srtDir",
        description="Sort direction.  Default is `desc`.",
        example="asc",
    )
    srt_key: Optional[EventSearchTerm] = Field(
        None, alias="srtKey", description="Search term for sorting.", example="event.id"
    )


class Source(BaseModel):
    category: Optional[str] = Field(
        None,
        description="General category of where the file originated. For example: Cloud Storage, Email, Social Media.",
        example="Social Media",
    )
    domain: Optional[str] = Field(
        None,
        description="Fully qualified domain name (FQDN) for the user's device at the time the event is recorded.  If the device is unable to resolve the domain name of the host, it reports the IP address of the host.",
        example="localhost",
    )
    domains: Optional[List[str]] = Field(
        None,
        description="The domain section of the URLs reported in source.tabs.url. (Note: Although similar in name, this field has no relation to source.domain, which reports the FQDN or IP address of the user’s device.)",
    )
    email: Optional[SourceEmail] = Field(
        None, description="Metadata about the email source."
    )
    ip: Optional[str] = Field(
        None,
        description="The external IP address of the user's device.",
        example="127.0.0.1",
    )
    name: Optional[str] = Field(
        None,
        description="The name reported by the device's operating system.  This may be different than the device name in the Code42 console.",
        example="Mari's MacBook",
    )
    operating_system: Optional[str] = Field(
        None,
        alias="operatingSystem",
        description="The operating system of the source device.",
        example="Windows 10",
    )
    private_ip: List[str] = Field(
        ...,
        alias="privateIp",
        description="The IP address of the user's device on your internal network, including Network interfaces, Virtual Network Interface controllers (NICs), and Loopback/non-routable addresses.",
        example=["127.0.0.1", "127.0.0.2"],
    )
    removable_media: Optional[RemovableMedia] = Field(
        None,
        alias="removableMedia",
        description="Metadata about the removable media source.",
    )
    tabs: Optional[List[Tab]] = Field(
        None, description="Metadata about the browser tab source."
    )


class Event(BaseModel):
    action: Optional[str] = Field(
        None,
        description="The rule_type of file event observed. For example: file-modified, application-read, removable-media-created.",
        example="file-downloaded",
    )
    id: str = Field(
        ...,
        description="The unique identifier for the event.",
        example="0_147e9445-2f30-4a91-8b2a-9455332e880a_973435567569502913_986467523038446097_163",
    )
    ingested: Optional[datetime] = Field(
        None,
        description="Date and time the event was initially received by Code42; timestamp is based on the Code42 server system clock and reported in Coordinated Universal Time (UTC).",
        example="2020-10-27T15:15:05.369203Z",
    )
    inserted: Optional[datetime] = Field(
        None,
        description="Date and time the event processing is completed by Code42; timestamp is based on the Code42 server system clock and reported in Coordinated Universal Time (UTC). Typically occurs very soon after the event.ingested time.",
        example="2020-10-27T15:16:05.369203Z",
    )
    observer: Optional[str] = Field(
        None,
        description="The data source that captured the file event. For example: GoogleDrive, Office365, Salesforce.",
        example="Endpoint",
    )
    related_events: Optional[List[RelatedEvent]] = Field(
        None,
        alias="relatedEvents",
        description="List of other events associated with this file. This can help determine the origin of the file.",
    )
    share_type: Optional[List[str]] = Field(
        None,
        alias="shareType",
        description="Sharing types added by this event.",
        example=["SharedViaLink"],
    )


class ExportRequestSearchTermV1(BaseModel):
    EventSearchTerms: Optional[List[EventSearchTerm]] = Field(
        None,
        description="Which EventSearchTerms to include in the output. If none is provided, all available EventSearchTermswill be output in an unspecified, not-guaranteed order.",
        example=["eventId", "eventType"],
    )
    group_clause: Optional[GroupClause] = Field(
        None,
        alias="groupClause",
        description="Grouping clause for any specified groups.  Default is `AND`.",
        example="OR",
    )
    groups: List[FilterGroupSearchTermV1] = Field(
        ..., description="One or more FilterGroups to be combined in a query."
    )
    srt_dir: Optional[SortDirection] = Field(
        None,
        alias="srtDir",
        description="Sort direction.  Default is `desc`.",
        example="asc",
    )
    srt_key: Optional[EventSearchTerm] = Field(
        None, alias="srtKey", description="Search term for sorting."
    )


class ExportRequestSearchTermV2(BaseModel):
    EventSearchTerms: Optional[List[EventSearchTerm]] = Field(
        None,
        description="Which EventSearchTerms to include in the output. If none is provided, all available EventSearchTermswill be output in an unspecified, not-guaranteed order.",
        example=["file.name", "file.directory"],
    )
    group_clause: Optional[GroupClause] = Field(
        None,
        alias="groupClause",
        description="Grouping clause for any specified groups.  Default is `AND`.",
        example="OR",
    )
    groups: List[FilterGroupSearchTermV2] = Field(
        ..., description="One or more FilterGroups to be combined in a query."
    )
    srt_dir: Optional[SortDirection] = Field(
        None,
        alias="srtDir",
        description="Sort direction.  Default is `desc`.",
        example="asc",
    )
    srt_key: Optional[EventSearchTerm] = Field(
        None, alias="srtKey", description="Search term for sorting."
    )


class FileEventResponseV1(BaseModel):
    file_events: Optional[List[FileEventV1]] = Field(
        None, alias="fileEvents", description="List of file events in the response."
    )
    next_pg_token: Optional[str] = Field(
        None,
        alias="nextPgToken",
        description="Use as the pgToken value in another request to indicate the starting point for additional page results. nextPgToken is null if there are no more results or if pgToken was not supplied.",
        example="0_147e9445-2f30-4a91-8b2a-9455332e880a_973435567569502913_986467523038446097_163",
    )
    problems: Optional[List[QueryProblemSearchTermV1]] = Field(
        None,
        description="List of problems in the request.  A problem with a search request could be an invalid filter value, an operator that can't be used on a term, etc.",
    )
    total_count: Optional[int] = Field(
        None,
        alias="totalCount",
        description="Total number of file events in the response.",
        example=42,
    )


class FileEventV2(ResponseModel):
    _timestamp: Optional[datetime] = Field(
        None,
        alias="@timestamp",
        description="Date and time that the Code42 service on the device detected an event; based on the device’s system clock and reported in Coordinated Universal Time (UTC).",
        example="2020-10-27T15:16:05.369203Z",
    )
    destination: Optional[Destination] = Field(
        None, description="Metadata about the destination of the file event."
    )
    event: Optional[Event] = Field(
        None, description="Summary information about the event."
    )
    file: Optional[File] = Field(
        None, description="Metadata about the file for this event."
    )
    process: Optional[Process] = Field(
        None, description="Metadata about the process associated with the event."
    )
    report: Optional[Report] = Field(
        None,
        description="Metadata for reports from 3rd party sources, such Salesforce downloads.",
    )
    risk: Optional[Risk] = Field(None, description="Risk factor metadata.")
    source: Optional[Source] = Field(
        None, description="Metadata about the source of the file event."
    )
    user: Optional[User] = Field(
        None,
        description="Attributes of the the Code42 username signed in to the Code42 app on the device.",
    )


class GroupingResponseSearchTermV1(BaseModel):
    groups: Optional[List[Group]] = Field(
        None, description="The top groups based on the query and group by term."
    )
    problems: Optional[List[QueryProblemSearchTermV1]] = Field(
        None,
        description="List of problems in the request.  A problem with a search request could be an invalid filter value, an operator that can't be used on a term, etc.",
    )


class GroupingResponseSearchTermV2(BaseModel):
    groups: Optional[List[Group]] = Field(
        None, description="The top groups based on the query and group by term."
    )
    problems: Optional[List[QueryProblemSearchTermV2]] = Field(
        None,
        description="List of problems in the request.  A problem with a search request could be an invalid filter value, an operator that can't be used on a term, etc.",
    )


class FileEventResponseV2(ResponseModel):
    file_events: Optional[List[FileEventV2]] = Field(
        None, alias="fileEvents", description="List of file events in the response."
    )
    next_pg_token: Optional[str] = Field(
        None,
        alias="nextPgToken",
        description="Use as the pgToken value in another request to indicate the starting point for additional page results. nextPgToken is null if there are no more results or if pgToken was not supplied.",
        example="0_147e9445-2f30-4a91-8b2a-9455332e880a_973435567569502913_986467523038446097_163",
    )
    problems: Optional[List[QueryProblemSearchTermV2]] = Field(
        None,
        description="List of problems in the request.  A problem with a search request could be an invalid filter value, an operator that can't be used on a term, etc.",
    )
    total_count: Optional[int] = Field(
        None,
        alias="totalCount",
        description="Total number of file events in the response.",
        example=42,
    )
