"""Loaders that map external corpora onto the Decision schema.

One module per validation tier:

- ``github_issues`` — V3, natural maintainer decisions on feature requests.

Planned: ``reqpairs`` (V1 conflict/duplicate corpora), ``gym`` (V2
ReqElicitBench), ``industrial`` (V4 anonymized company cases).
"""

__all__ = ["github_issues"]
