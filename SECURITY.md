# Security policy

Context Kit is designed to reduce accidental disclosure when creating repository context, but it is not a complete secrets scanner. Always inspect a generated bundle before sharing it.

## Reporting a vulnerability

Please do not include live credentials, private keys, or other sensitive values in a public issue. Use GitHub's private vulnerability reporting for this repository when it is available. If it is unavailable, open a minimal issue asking for a private contact channel and do not include the secret itself.

Include the affected version, a safe reproduction, and the expected versus observed behavior. Rotate any credential that may have been exposed while preparing the report.

## Scope

Reports about missed secret formats, unsafe file discovery, path traversal, or accidental inclusion of binary data are especially useful. A rule that intentionally excludes a file should be documented and covered by a test.
