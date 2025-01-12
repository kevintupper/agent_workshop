# -----------------------------------------------------------------------------------------------------
# rga_types.py
# -----------------------------------------------------------------------------------------------------
#
# This module contains Python models that represent the data structures for the Regulations.gov api.
#



# -----------------------------------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------------------------------

from typing import List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


# -----------------------------------------------------------------------------------------------------
# Enums
# -----------------------------------------------------------------------------------------------------

class DocumentTypestring(str, Enum):
    """
    Type of document. This field is always returned in JSON response.

    Allowed values: Notice, Rule, Proposed Rule, Supporting & Related Material, Other
    """
    NOTICE = "Notice"
    RULE = "Rule"
    PROPOSED_RULE = "Proposed Rule"
    SUPPORTING_RELATED_MATERIAL = "Supporting & Related Material"
    OTHER = "Other"


class DocketTypestring(str, Enum):
    """
    the type of docket

    Allowed values: Rulemaking, Nonrulemaking
    """
    RULEMAKING = "Rulemaking"
    NONRULEMAKING = "Nonrulemaking"


class SubmitterTypestring(str, Enum):
    """
    the submitter type

    Allowed values: Anonymous, Individual, Organization
    """
    ANONYMOUS = "Anonymous"
    INDIVIDUAL = "Individual"
    ORGANIZATION = "Organization"


# -----------------------------------------------------------------------------------------------------
# Shared Models
# -----------------------------------------------------------------------------------------------------

class SelfLink(BaseModel):
    """
    Represents a link to the resource itself.
    """
    self: str = Field(..., description="A string containing the link URL.")


class FindAllResponseMetadata(BaseModel):
    """
    Metadata for the findAll response.
    """
    hasNextPage: bool = Field(..., description="Whether there is a next page.")
    hasPreviousPage: bool = Field(..., description="Whether there is a previous page.")
    numberOfElements: int = Field(..., description="Number of elements (documents, comments, dockets) that matched the search criteria.")
    pageNumber: int = Field(..., description="Current page number.")
    pageSize: int = Field(..., description="Size of each page. Maximum page size is 250.")
    totalElements: int = Field(..., description="Total elements overall.")
    totalPages: int = Field(..., description="Total number of pages. Maximum total pages is 200.")
    firstPage: bool = Field(..., description="Is this the first page?")
    lastPage: bool = Field(..., description="Is this the last page?")

class FileFormat(BaseModel):
    """
    Represents a file format associated with a document or attachment.
    """
    fileUrl: str = Field(..., description="URL of the file on S3.")
    format: str = Field(..., description="The format of the file such as pdf.")
    size: int = Field(..., description="The file size in bytes.")


class Attachment(BaseModel):
    """
    Represents an attachment associated with a document.
    """
    agencyNote: Optional[str] = Field(None, description="The note by the agency.")
    authors: Optional[List[str]] = Field(None, description="The individual, organization, or group of collaborators that contributed to the creation of the attachment.")
    docAbstract: Optional[str] = Field(None, description="The detailed description of the attachment.")
    docOrder: int = Field(..., description="The order of the attachment.")
    fileFormats: List[FileFormat] = Field(..., description="List of file formats associated with the attachment.")
    modifyDate: datetime = Field(..., description="The date when the attachment was last modified. ISO 8601 format.")
    publication: Optional[str] = Field(None, description="The publication date of the attachment.")
    restrictReason: Optional[str] = Field(None, description="If the attachment is restricted, this field will state the reason.")
    restrictReasonType: Optional[str] = Field(None, description="If the attachment is restricted, this field will state the type of restriction.")
    title: str = Field(..., description="The formal title of the attachment.")


class AttachmentFindAllItem(BaseModel):
    """
    Represents a single attachment in the list.
    """
    id: str = Field(..., description="The JSON:API resource ID attachmentId.")
    type: str = Field(..., description="The JSON:API resource type attachments.")
    attributes: Attachment = Field(..., description="A single Attachment object.")
    links: Union[SelfLink, List[SelfLink]] = Field(..., description="A single link or a list of links to self.")


class RelationshipLinks(BaseModel):
    """
    Relationship links to other related resources (attachments).
    """
    self: str = Field(..., description="A string containing the self link URL.")
    related: str = Field(..., description="A string containing the related link URL.")


class RelationshipToAttachment(BaseModel):
    """
    Represents a relationship to an attachment.
    """
    type: str = Field(..., description="The JSON:API resource type.")
    id: str = Field(..., description="The JSON:API resource ID.")


class Relationship(BaseModel):
    """
    Represents relationships to other related resources (attachments).
    """
    data: Optional[List[RelationshipToAttachment]] = Field(None, description="The data field containing related resources.")
    links: Optional[RelationshipLinks] = Field(None, description="Links to related resources.")


# -----------------------------------------------------------------------------------------------------
# Document Models and Models Returned by the API for get_documents and get_document_by_id
# -----------------------------------------------------------------------------------------------------

class Document(BaseModel):
    """
    Represents a single document with its attributes.
    """
    agencyId: str = Field(..., description="The acronym used to abbreviate the name of the agency associated with the document.")
    commentEndDate: Optional[datetime] = Field(None, description="The date that closes the period when public comments may be submitted on the document. ISO 8601 format.")
    commentStartDate: Optional[datetime] = Field(None, description="The date that begins the period when public comments may be submitted on the document. ISO 8601 format.")
    docketId: str = Field(..., description="The ID of the docket to which the document corresponds.")
    documentType: DocumentTypestring = Field(..., description="Type of document. This field is always returned in JSON response.")
    frDocNum: Optional[str] = Field(None, description="The federal register document number of the document.")
    highlightedContent: Optional[str] = Field(None, description="Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.")
    lastModifiedDate: datetime = Field(..., description="The date document was last modified in the system. ISO 8601 format.")
    objectId: str = Field(..., description="The internal ID of the document in our system.")
    openForComment: bool = Field(..., description="Conveys if the document is open for comment.")
    postedDate: datetime = Field(..., description="The date that the document was posted by the agency to the system. ISO 8601 format.")
    subtype: Optional[str] = Field(None, description="An agency-specific attribute to further categorize a document beyond the type (documentType).")
    title: str = Field(..., description="The formal title of the document.")
    withdrawn: bool = Field(..., description="Conveys if the document is withdrawn.")

class DocumentFindAllItem(BaseModel):
    """
    Represents a single document in the list.
    """
    id: str = Field(..., description="The JSON:API resource ID documentId.")
    type: str = Field(..., description="The JSON:API resource type documents.")
    attributes: Document = Field(..., description="A single Document object.")
    links: Union[SelfLink, List[SelfLink]] = Field(..., description="A single link or a list of links to self.")

class DocumentFindAllResponse(BaseModel):
    """
    A JSON:API document with a list of resources.

    This is returned by the /documents endpoint which we call with the get_documents function.

    """
    data: List[DocumentFindAllItem] = Field(..., description="The list of documents where each document is a JSON:API document.")
    meta: FindAllResponseMetadata = Field(..., description="A JSON:API document with metadata for findAll.")

class DocumentDetail(BaseModel):
    """
    Represents detailed attributes of a single document.
    """
    address1: Optional[str] = Field(None, description="The first line of the submitter's address.")
    address2: Optional[str] = Field(None, description="The second line of the submitter's address.")
    agencyId: str = Field(..., description="The acronym used to abbreviate the name of the agency associated with the document.")
    city: Optional[str] = Field(None, description="The city associated with the submitter's address.")
    category: Optional[str] = Field(None, description="An agency-specific category allowing agencies to group comments according to their type.")
    comment: Optional[str] = Field(None, description="The comment associated with the document.")
    country: Optional[str] = Field(None, description="The country associated with the submitter's address.")
    docAbstract: Optional[str] = Field(None, description="The detailed description or abstract of the document.")
    docketId: str = Field(..., description="The ID of the docket to which the document corresponds.")
    documentType: DocumentTypestring = Field(..., description="Type of document. This field is always returned in JSON response.")
    email: Optional[str] = Field(None, description="The submitter's e-mail address.")
    fax: Optional[str] = Field(None, description="The submitter's fax number.")
    field1: Optional[str] = Field(None, description="An agency-specific field used for storing additional data with the document.")
    field2: Optional[str] = Field(None, description="An agency-specific field used for storing additional data with the document.")
    fileFormats: List[FileFormat] = Field(..., description="List of file formats associated with the document.")
    firstName: Optional[str] = Field(None, description="The submitter's first name.")
    govAgency: Optional[str] = Field(None, description="The name of the government agency that the submitter represents.")
    govAgencyType: Optional[str] = Field(None, description="The type of government agency that the submitter represents.")
    lastName: Optional[str] = Field(None, description="The submitter's last name.")
    legacyId: Optional[str] = Field(None, description="An agency-specific identifier that was given to the document in the legacy system.")
    modifyDate: datetime = Field(..., description="The date when the document was last modified. ISO 8601 format.")
    objectId: str = Field(..., description="The internal ID of the document in our system.")
    openForComment: bool = Field(..., description="Conveys if a document is open for comment.")
    organization: Optional[str] = Field(None, description="The organization that the submitter represents.")
    originalDocumentId: Optional[str] = Field(None, description="The document ID that was assigned when first entered into the system.")
    pageCount: Union[int, str, None] = Field(None, description="Conveys the number of pages contained in the document.")
    phone: Optional[str] = Field(None, description="The submitter's phone number.")
    postedDate: datetime = Field(..., description="The date that the document was posted by the agency to the system. ISO 8601 format.")
    postmarkDate: Optional[datetime] = Field(None, description="The postmark date of a document that was sent by mail.")
    reasonWithdrawn: Optional[str] = Field(None, description="If the document is withdrawn, this field will state the reason.")
    receiveDate: datetime = Field(..., description="The date that the document was received by the agency to the system. ISO 8601 format.")
    restrictReason: Optional[str] = Field(None, description="If the document is restricted, this field will state the reason.")
    restrictReasonType: Optional[str] = Field(None, description="If the document is restricted, this field will state the type of restriction.")
    stateProvinceRegion: Optional[str] = Field(None, description="The submitter's state, province, or region.")
    subtype: Optional[str] = Field(None, description="An agency-specific attribute to further categorize a document beyond the documentType.")
    title: str = Field(..., description="The formal title of the document.")
    trackingNbr: Optional[str] = Field(None, description="The tracking number of the submission.")
    withdrawn: bool = Field(..., description="Conveys if the document is withdrawn.")
    zip: Optional[str] = Field(None, description="The zip associated with the submitter's address.")
    additionalRins: Optional[List[str]] = Field(None, description="One or more Regulatory Information Numbers (RINs) to which the document relates.")
    allowLateComments: bool = Field(..., description="Indicates whether the owning agency will accept comments on the document after the due date.")
    authorDate: Optional[datetime] = Field(None, description="The date that the authors wrote or published the document.")
    authors: Optional[List[str]] = Field(None, description="The individual, organization, or group of collaborators that contributed to the creation of the document.")
    cfrPart: Optional[str] = Field(None, description="The Code of Federal Regulations (CFR) Citation applicable to the document.")
    commentEndDate: Optional[datetime] = Field(None, description="The date that closes the period when public comments may be submitted on the document.")
    commentStartDate: Optional[datetime] = Field(None, description="The date that begins the period when public comments may be submitted on the document.")
    effectiveDate: Optional[datetime] = Field(None, description="The date the document is put into effect.")
    exhibitLocation: Optional[str] = Field(None, description="The physical location of an exhibit to which a document refers.")
    exhibitType: Optional[str] = Field(None, description="The type of exhibit to which a document refers.")
    frDocNum: Optional[str] = Field(None, description="The unique identifier of a document originating in the Federal Register.")
    frVolNum: Optional[str] = Field(None, description="The Federal Register volume number where the document was published.")
    implementationDate: Optional[datetime] = Field(None, description="The date the document is to be implemented.")
    media: Optional[str] = Field(None, description="The media in which the document is stored.")
    ombApproval: Optional[str] = Field(None, description="The control number assigned when approval is given by the Office of Management and Budget (OMB).")
    paperLength: Optional[int] = Field(None, description="When the document is in paper format, indicates the length of the paper.")
    paperWidth: Optional[int] = Field(None, description="When the document is in paper format, indicates the width of the paper.")
    regWriterInstruction: Optional[str] = Field(None, description="Additional instructions provided by the writer of the regulation.")
    sourceCitation: Optional[str] = Field(None, description="The citation for the source that published the document.")
    startEndPage: Optional[str] = Field(None, description="The starting and ending pages where the document was published.")
    subject: Optional[str] = Field(None, description="The subject of the document.")
    topics: Optional[List[str]] = Field(None, description="The principal topics to which the document pertains.")

class DocumentFindOneItem(BaseModel):
    """
    A JSON:API document which represents a single document.
    """
    id: str = Field(..., description="The JSON:API resource ID (documentId of the document).")
    type: str = Field(..., description="The JSON:API resource type documents.")
    attributes: DocumentDetail = Field(..., description="Detailed attributes of the document.")
    relationships: Optional[Relationship] = Field(None, description="Relationships to other related resources (attachments).")
    links: Union[SelfLink, List[SelfLink]] = Field(..., description="A single link or a list of links to self.")

class DocumentFindOneResponse(BaseModel):
    """
    A JSON:API document which represents a single document.
    """
    data: DocumentFindOneItem = Field(..., description="A single DocumentFindOneItem object.")
    included: Optional[List[AttachmentFindAllItem]] = Field(None, description="The list of attachments included in the response.")



