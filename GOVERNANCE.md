# ProfileForge Governance

This document describes the governance model for the ProfileForge open-source project.

## Model: Benevolent Dictator with Core Maintainer Team

ProfileForge operates under a **Benevolent Dictator for Life (BDFL)** model supplemented
by a **Core Maintainer Team**. The BDFL holds final authority on project direction and
breaking decisions, but governance is conducted collaboratively in practice.

This model is designed to maximize responsiveness and quality during early-stage development
while providing clear accountability and a path toward broader community governance as the
project matures.

## Roles

### BDFL (Benevolent Dictator)

- Holds ultimate authority on project direction, architecture, and release timing
- Can veto any proposed change that conflicts with the project's core values or roadmap
- Responsible for maintaining the integrity of the public API
- Commits to acting in the best interest of the project and its community

### Core Maintainers

Core Maintainers are trusted contributors who:

- Have demonstrated sustained, high-quality contributions over time
- Have commit access to the main repository
- Review and merge pull requests
- Triage issues and manage the backlog
- Participate in RFC discussions and vote on proposals

Becoming a Core Maintainer requires a history of sustained contributions and community trust.

### Contributors

Anyone who opens issues, submits PRs, writes documentation, or participates in
discussions is a **Contributor**. All contributors are valued members of the community.

Contribution guidelines are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Decision-Making Process

### Day-to-Day Decisions (Consensus)

For most changes — bug fixes, documentation improvements, minor enhancements, new
widgets, and new themes — the process is:

1. Open an issue or PR describing the change
2. Core Maintainers review and provide feedback
3. Once two Core Maintainers approve (or the BDFL approves), the change can be merged
4. **Consensus is preferred** over voting; we aim for agreement, not supermajority wins

### Significant Changes (Lazy Consensus)

For changes that affect architecture, dependencies, or development tooling:

1. Open an issue with a proposal, tagged `proposal`
2. Allow **7 days** for community and maintainer feedback
3. If no substantive objections are raised (lazy consensus), the change proceeds
4. If objections are raised, discussion continues until consensus is reached or escalated

### API Changes (RFC Required)

Any change that modifies or extends the **public API surface** — including new CLI
commands, new widget base class methods, changes to `manifest.yaml` schema, or changes
to theme token keys — **requires a formal RFC**.

The RFC process is documented in [docs/RFC_PROCESS.md](docs/RFC_PROCESS.md).

RFC steps:
1. Author submits an RFC document in `docs/rfcs/` following the RFC template
2. RFC is discussed for a minimum of **14 days**
3. Core Maintainers vote (majority required); BDFL holds veto power
4. Accepted RFCs are tracked in the ADR log (`docs/adr/`)

### Breaking Changes (Maintainer Veto)

Changes that break backward compatibility with the existing public API require:

1. A completed and accepted RFC
2. Explicit sign-off from **the BDFL or a majority of Core Maintainers**
3. A **deprecation notice** in the previous minor release before the breaking change ships

**Any Core Maintainer may veto a breaking change** by raising a formal objection.
The veto must be accompanied by a written explanation and an alternative proposal.

## Conflict Resolution

1. Discussion in the relevant issue or PR is the first step
2. If discussion is unproductive, the BDFL makes a final ruling
3. The BDFL's ruling is documented in the relevant issue for transparency

## Release Authority

Releases are authorized by:

- The BDFL, or
- A Core Maintainer with explicit written delegation from the BDFL

The release process is documented in [docs/RELEASE_GUIDE.md](docs/RELEASE_GUIDE.md).

## Amendments to Governance

Changes to this governance document require:

1. An RFC submitted to `docs/rfcs/`
2. A 30-day community review period
3. Approval by the BDFL

## Code of Conduct

All participants in the ProfileForge community are expected to follow the
[Code of Conduct](CODE_OF_CONDUCT.md). Enforcement is handled by Core Maintainers,
with the BDFL as the final escalation point.

---

*This governance model is designed to evolve. As the community grows, we expect
to transition toward a more distributed, committee-based model aligned with
established open-source foundations.*
