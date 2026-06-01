# S4Luminus Upgrade Impact - Knowledge Source

## Context
- Source system upgrade is moving from ECC to S/4HANA.
- SAP table structures are changing for data that flows into DWH.
- Impact analysis is known at ECC extraction level, including where impacted tables exist in the extraction layer.

## Impact Summary
- Around 24 extraction flows are impacted.
- Primary layer impact starts at EL and propagates to AL and PL tables.
- Qlik reports are impacted (reference: Jan Floren list).
- Qlik reports depend on both AL and PL layers.

## Current Progress
- Bart de Wal is already implementing field changes on EL side.
- Work is currently happening in DWH sandbox with ECC sandbox.
- Work has not started yet on AL, PL, FL, and ML table adaptations.

## Data and Reporting Scope
- Impact levels are categorized as heavy impact, low impact (1-2 fields), and no impact.
- Each report is treated as a separate use case.
- EL and PL impacted table lists are available.
- Additional flows exist via NEO/SADP CADPs; likely not relevant for Qlik unless those specific flows are consumed.
- SAS report dependency exists from AL layer (owner noted as Hans).
- WebI is out of scope (major part already done in Cogenius).

## Timeline and Milestones
- Intake starts in May/June (2.5-2.6 window noted).
- SAP test switch planned in August.
- SAP acceptance switch planned in November.
- S/4 instance runs in parallel until cutover.
- Target go-live year is 2027.
- Development target: PI3.
- Testing readiness target: PI4.

## Environment Needs
- A separate linked environment is needed to test the full end-to-end flow.

## Open Questions
- Who is the business owner per impacted report/use case?
- What is the exact Q3 and Q4 scope for critical/prioritized use cases (for example utility contracts, churn)?

## Working Contacts
- Devashish Jain
- Hans
- Jan Floren
- Bart de Wal
