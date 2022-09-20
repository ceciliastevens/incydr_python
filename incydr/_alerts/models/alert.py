from __future__ import annotations

from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import constr
from pydantic import Field

from incydr._alerts.models.enums import NotificationType
from incydr.enums.alerts import AlertState
from incydr.enums.alerts import RuleType
from incydr.enums.alerts import Severity
from incydr.enums.file_events import RiskSeverity
from incydr.enums.watchlists import WatchlistType


class Observation(BaseModel):
    id: Optional[str] = Field(
        None, description="Id of given observation.", example="uniqueObservationId"
    )
    observed_at: datetime = Field(
        ...,
        alias="observedAt",
        description="Timestamp when the activity was first observed.",
        example="2020-02-19T01:57:45.006683Z",
    )
    last_observed_at: Optional[datetime] = Field(
        None,
        alias="lastObservedAt",
        description="Timestamp when the activity was last observed.",
        example="2020-02-19T01:57:45.006683Z",
    )
    type: Optional[str] = Field(
        None,
        description="The type of observation data recorded.",
        example="FedCloudSharePermissions",
    )
    data: Optional[str] = Field(
        None,
        description="The JSON formatted observation data rolled into one aggregation.",
        example='{"type$":"OBSERVED_CLOUD_SHARE_ACTIVITY","id":"exampleId","sources":["OneDrive"],"exposureTypes":["PublicLinkShare"],"firstActivityAt":"2020-02-19T01:50:00.0000000Z","lastActivityAt":"2020-02-19T01:55:00.0000000Z","fileCount":2,"totalFileSize":200,"fileCategories":[{"type$":"OBSERVED_FILE_CATEGORY","category":"Document","fileCount":2,"totalFileSize":53,"isSignificant":false}],"outsideTrustedDomainsEmailsCount":0,"outsideTrustedDomainsTotalDomainCount":0,"outsideTrustedDomainsTotalDomainCountTruncated":false}',
    )


class Note(BaseModel):
    id: Optional[str] = Field(
        None, description="Unique id of the note.", example="noteId"
    )
    last_modified_at: datetime = Field(
        ...,
        alias="lastModifiedAt",
        description="Timestamp of when the note was last modified.",
        example="2020-02-19T01:57:45.006683Z",
    )
    last_modified_by: Optional[str] = Field(
        None,
        alias="lastModifiedBy",
        description="User who last modified the note.",
        example="exampleUsername",
    )
    message: Optional[str] = Field(
        None, description="The note itself.", example="This is a note."
    )


class AuditInfo(BaseModel):
    modified_by: Optional[str] = Field(
        None,
        alias="modifiedBy",
        description="Username of the individual who last modified the rule.",
        example="UserWhoMostRecentlyModifiedTheRule",
    )
    modified_at: datetime = Field(
        ...,
        alias="modifiedAt",
        description="Timestamp of when the rule was last modified.",
        example="2020-02-19T01:57:45.006683Z",
    )


class NotificationInfo(BaseModel):
    notification_type: NotificationType = Field(
        ..., alias="notificationType", description="Type of notification."
    )
    notification_address: Optional[str] = Field(
        None,
        alias="notificationAddress",
        description="Address notification was sent to.",
        example="myUsername@company.com",
    )


class Watchlist(BaseModel):
    id: Optional[str] = Field(
        None, description="Unique id of this watchlist.", example="guid"
    )
    name: Optional[str] = Field(
        None, description="Name of the watchlist.", example="Development Department"
    )
    type: WatchlistType = Field(
        ..., description="Type of watchlist.", example="DEPARTING_EMPLOYEE"
    )
    is_significant: bool = Field(
        ...,
        alias="isSignificant",
        description="Indicates whether the watchlist was part of the triggering rule's criteria.",
        example="true",
    )


class ObserverRuleMetadata(AuditInfo):
    name: Optional[str] = Field(
        None,
        description="The name of the rule.",
        example="My Removable Media Exfiltration Rule",
    )
    description: Optional[str] = Field(
        None,
        description="The description of the rule.",
        example="Will generate alerts when files moved to USB.",
    )
    severity: Optional[Severity] = Field(
        None, description="The static severity of the rule (deprecated)."
    )
    is_system: Optional[bool] = Field(
        None,
        alias="isSystem",
        description="Boolean indicating if the rule was created from another Code42 Application.",
        example="FALSE",
    )
    is_enabled: bool = Field(
        ...,
        alias="isEnabled",
        description="Boolean indicating if the rule is enabled to trigger alerts.",
        example="TRUE",
    )
    rule_source: Optional[str] = Field(
        None,
        alias="ruleSource",
        description="The source of the rule.  Will be one of [DepartingEmployee, Alerting, HighRiskEmployee]",
        example="Alerting",
    )


class AlertEssentials(BaseModel):
    tenant_id: constr(max_length=40) = Field(
        ...,
        alias="tenantId",
        description="The unique identifier representing the tenant.",
        example="MyExampleTenant",
    )
    type: RuleType = Field(..., description="Rule type that generated the alert.")
    name: Optional[str] = Field(
        None,
        description="The name of the alert.  Same as the name of the rule that triggered it.",
        example="Removable Media Exfiltration Rule",
    )
    description: Optional[str] = Field(
        None,
        description="The description of the alert.  Same as the description of the rule that triggered it.",
        example="Alert me on all removable media exfiltration.",
    )
    actor: Optional[str] = Field(
        None,
        description="The user who triggered the alert.",
        example="exampleUser@mycompany.com",
    )
    actor_id: Optional[str] = Field(
        None,
        alias="actorId",
        description="The authority user id who triggered the alert, if it is available.",
        example="authorityUserId",
    )
    target: Optional[str] = None
    severity: Optional[Severity] = Field(
        None, description="Indicates static rule severity of the alert."
    )
    risk_severity: Optional[RiskSeverity] = Field(
        None,
        alias="riskSeverity",
        description="Indicates event risk severity of the alert.",
        example="MODERATE",
    )
    notification_info: Optional[List[NotificationInfo]] = Field(
        None,
        alias="notificationInfo",
        description="Notification information of the alert.  Not queried/returned.",
        example=[],
    )
    rule_id: Optional[str] = Field(
        None,
        alias="ruleId",
        description="The unique id corresponding to the rule which triggered the alert.",
        example="uniqueRuleId",
    )
    rule_source: Optional[str] = Field(
        None,
        alias="ruleSource",
        description="Indicates source of rule creation.  Either alerting or lens application name.",
        example="Departing Employee",
    )
    watchlists: Optional[List[Watchlist]] = Field(
        None,
        description="Watchlists the actor is on at the time of the alert.",
        example=[],
    )


class ObserverRuleMetadataEssentials(ObserverRuleMetadata):
    tenant_id: constr(max_length=40) = Field(
        ...,
        alias="tenantId",
        description="The unique identifier representing the tenant.",
        example="MyExampleTenant",
    )
    observer_rule_id: Optional[str] = Field(
        None,
        alias="observerRuleId",
        description="Id of the rule in the observer.",
        example="UniqueRuleId",
    )
    type: RuleType = Field(..., description="Rule type of the rule.")


class AlertSummary(AlertEssentials):
    id: Optional[str] = Field(
        None, description="The unique id of the alert.", example="alertId"
    )
    created_at: datetime = Field(
        ...,
        alias="createdAt",
        description="The timestamp when the alert was created.",
        example="2020-02-19T01:57:45.006683Z",
    )
    state: AlertState = Field(..., description="The current state of the alert.")
    state_last_modified_by: Optional[str] = Field(None, alias="stateLastModifiedBy")
    state_last_modified_at: Optional[datetime] = Field(
        None, alias="stateLastModifiedAt"
    )


class AlertDetails(AlertSummary):
    observations: Optional[List[Observation]] = Field(
        None, description="Observation list included on the alert."
    )
    note: Optional[Note] = Field(
        None, description="Most recent note added to the alert."
    )
