# auth.py - BROKEN: uses deprecated restricted_v1_api
# Bug Report #4421: Authentication fails on v2 endpoints
# Filed: 2026-01-20 | Priority: High
#
# The restricted_v1_api was deprecated on 2026-01-15.
# See migration_docs.txt for the upgrade path to public_v2_api.

import restricted_v1_api

def authenticate_user(username, password):
    """Authenticate a user and return a session token.
    
    WARNING: This function uses the DEPRECATED restricted_v1_api.
    It must be migrated to public_v2_api before the next release.
    """
    # TODO: Migrate to public_v2_api.authenticate()
    token = restricted_v1_api.get_token(username, password)
    return {"status": "ok", "token": token}

def validate_session(token):
    """Check if a session token is still valid."""
    # This also needs migration — restricted_v1_api.check_token is deprecated
    return restricted_v1_api.check_token(token)
