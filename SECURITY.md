# Security Policy

## Supported Versions

The following versions of ProfileForge are currently supported with security updates:

| Version       | Supported          |
| ------------- | ------------------ |
| 1.0.0-rc1     | ✅ Supported        |
| < 1.0.0-rc1   | ❌ Not supported    |

Once v1.0.0 is officially released, it will become the primary supported version.
The RC1 release is supported for the duration of the release-candidate feedback window.

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities via public GitHub Issues.**

If you discover a security vulnerability in ProfileForge, please report it responsibly
by sending an email to:

**security@profileforge.dev**

### What to Include in Your Report

Please provide as much information as possible to help us understand and reproduce the issue:

- A clear description of the vulnerability and its potential impact
- Steps to reproduce the issue or a proof-of-concept (PoC)
- The ProfileForge version affected
- Your environment details (OS, Python version)
- Any suggested mitigations if you have them

### Response Timeline

We take security disclosures seriously. You can expect the following:

| Action                        | Timeline                    |
| ----------------------------- | --------------------------- |
| **Acknowledgment**            | Within **48 hours**         |
| **Initial assessment**        | Within **5 business days**  |
| **Patch / fix delivered**     | Within **14 days**          |
| **Public disclosure**         | After patch is released     |

We will keep you informed of progress throughout the process. If for any reason
a fix cannot be delivered within 14 days, we will notify you with an updated timeline.

### Coordinated Disclosure

We follow a coordinated disclosure model:

1. Reporter submits the vulnerability privately.
2. We acknowledge, triage, and develop a fix.
3. A patch release is prepared and tested.
4. The fix is released, and a security advisory is published.
5. Full public disclosure occurs after affected users have had reasonable time to update.

We kindly ask that you do not publicly disclose the vulnerability until we have had
the opportunity to investigate and release a patch.

## Bug Bounty

ProfileForge is an open-source project maintained by community volunteers.
**We do not currently offer a monetary bug bounty program.**

We do, however, publicly recognize security researchers who responsibly disclose
vulnerabilities in our `CHANGELOG.md` and security advisories, with your permission.

## Out of Scope

The following are generally considered out of scope for security reports:

- Issues in third-party libraries (please report those upstream)
- Rate limiting on GitHub APIs (this is GitHub's infrastructure)
- Issues requiring physical access to a developer's machine
- Social engineering attacks

## Contact

For security disclosures: **security@profileforge.dev**  
For general conduct issues: **conduct@profileforge.dev**
