from enum import Enum


class PolicyTypeEnum(str, Enum):
    """p for policy, g for grouping"""

    p = "p"
    g = "g"


class ResourceDomainEnum(str, Enum):
    words = "words/"
    field_versions = "field_versions/"
    suggestions = "suggestions/"


class ResourceRightsEnum(str, Enum):
    """one user of one resource can only be one of the below"""

    own_word = "own_word_right"  # user is owner of the user resource
    own_field_version = "own_field_version_right"
    own_suggestion = "own_suggestion_right"
    admin = "admin_right"  # user is admin


class ResourceActionsEnum(str, Enum):
    """these are the actions"""

    # on specific word id
    update_word_title = "update_word_title"
    lock_word = "lock_word"
    merge_word = "merge_word"
    deactivate_word = "deactivate_word"

    # on specific field version id
    update_field_version_content = "update_field_version_content"
    deactivate_field_version = "deactivate_field_version"
    accept_or_reject_suggestion = "accept_or_reject_suggestion"

    # on specific suggestion
    update_suggestion_content = "update_suggestion_content"
    deactivate_suggestion = "deactivate_suggestion"



resource_right_action_mapping: dict = {
    ResourceRightsEnum.own_word: {
        ResourceActionsEnum.update_word_title,
    },
    ResourceRightsEnum.own_field_version: {
        ResourceActionsEnum.update_field_version_content,
        ResourceActionsEnum.accept_or_reject_suggestion,
    },
    ResourceRightsEnum.own_suggestion: {
        ResourceActionsEnum.update_suggestion_content,
        ResourceActionsEnum.deactivate_suggestion
    },
    ResourceRightsEnum.admin: {
        ResourceActionsEnum.update_word_title,
        ResourceActionsEnum.lock_word,
        ResourceActionsEnum.merge_word,
        ResourceActionsEnum.deactivate_field_version,
        ResourceActionsEnum.deactivate_suggestion,
        ResourceActionsEnum.deactivate_word
    },
}