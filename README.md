# Preflight

Preflight helps you produce requirements and designs that AI agents can use to deliver software
autonomously. Its goal is to make intended behaviour, business meaning, technical decisions, and
verification expectations clear enough for an agent to implement the change without inventing
missing rules or relying on the original conversation.

`define-change` establishes what should happen and what it means in the business. `design-solution`
explains how the system should deliver that behaviour. Both expose assumptions, unresolved
decisions, and evidence gaps so you can assess whether the outputs are fit for implementation.
Both can create, revise, recover, review, or validate material within their scope.

Give your agent the objective and relevant sources, define which decisions it may make, and ask it
to work within that scope. Pass the results to your chosen implementation workflow when ready.
Preflight prepares the change; implementation and delivery remain with that workflow.

Preflight is designed for largely autonomous work. You remain responsible for understanding the
inputs and assessing whether the outputs serve your purpose. The agent must explain its assumptions,
choices, evidence, and remaining questions so you can make that assessment.

## Choose where to start

Choose the skill that addresses your current uncertainty:

| Your task | Use | Ask for |
| --- | --- | --- |
| Establish what should happen and what it means in the business | [define-change](skills/define-change/README.md) | Requirements, acceptance examples, domain models, business diagrams and tables, or assessment of existing material. |
| Decide how the system should work | [design-solution](skills/design-solution/README.md) | Architecture, architectural decision records, technical designs, interface contracts, technical models, or assessment of existing material. |

Start with existing accepted documents where they suffice. Use either skill to resolve uncertainty,
recover what an existing system does, or assess material already available. Recovery distinguishes
observed behaviour from accepted requirements or design. You do not need to run both skills in sequence.

To start without installation, ask your agent to read the relevant `skills/<name>/SKILL.md` in this
checkout. After installation, invoke the skill by name using your agent's supported syntax.

## Supply useful inputs and decision boundaries

Before you leave the agent to work, supply the information it needs:

- Describe the problem, affected users, desired outcome, and exclusions.
- Provide relevant policies, examples, existing documents, and implementation access. Identify
  accepted decisions and distinguish them from proposals or observed behavior.
- State whether the agent should draft, revise, review, or validate. Name the files or
  concerns it may change. A review remains read-only unless you also request edits.
- Define which decisions the agent may make. If you delegate acceptance of requirements or designs,
  identify the artifacts, scope, and limits. Otherwise new governing content remains proposed.
- Give practical limits such as available tools, external access, time, and required checks.

Ask the agent to investigate available facts and make routine preparation choices within the
agreed scope. It should continue independent work when one consequential decision is unresolved.
A missing business decision can block dependent work. It must not become an invented rule.

If you cannot supply a formal specification, start with a problem, representative examples, and
sources you trust. Ask the agent to explain what it can establish and what remains uncertain.

## Map domain contexts

Ask `define-change` to draw a context map when you need to inspect meaning boundaries, translations
and relationships between domain models. It also analyses material contextual differences and
information restrictions during ordinary domain work, without adding an unrequested map.
Context relationships constrain design; they do not prescribe services or deployment units.

## Independent review of new or changed proposals

Draft and substantive Revise include [independent challenge](shared/independent-review.md),
including complete chat proposals and as-built recovery. The existing lead coordinates and may
also draft. The drafter owns edits. A separate reviewer first frames the concern from sources,
then challenges the candidate and checks material corrections. Review one coherent concern,
not each file separately. Reuse adequate independent review already supplied by your workflow.

Your host needs native independent-agent support and an available configured reviewer model.
The same model can draft and review in separate contexts. Without a suitable reviewer, the agent
returns useful work explicitly as unreviewed. Editorial edits, exploration and explanations are
exempt. Standalone Review and bounded Validate remain read-only and do not recursively delegate.
Review does not accept a proposal or authorize implementation. See the bounded
[agent exercise cases](tests/independent-review-cases.md) when verifying this behavior.

## Start with a short request

Name the task and subject. Point to relevant sources if they are not already clear from the
conversation or project. The skills already cover source checks, assumptions, exceptions, review,
and evidence appropriate to the task. You do not need to repeat those instructions.
If the task is already clear from the conversation, the skill name alone can be enough.

Add a particular output, format, or constraint when you need it. For example, ask for a domain
model as well as requirements, or name a diagram you want. "This policy" and "this change" in the
examples below refer to material already supplied or clearly identified in the project.

For requirements and domain meaning, try:

> $define-change Define cancellation requirements from this policy and code.

For architecture and technical design, try:

> $design-solution Design this change, including a context diagram.

For a read-only design review, try:

> $design-solution Review this design.

To resume work, provide the existing task record and current sources. Ask the agent to reconcile
completed work and evidence before continuing from the next executable action.

## Use supported models and Mermaid diagrams

For business and requirements models, use `define-change`. It covers domain concepts, terminology,
identity, relationships, events, and rules. Use aggregates to discuss what must change together,
and invariants for rules that must always hold. When you ask for modelling, the skill selects the
smallest useful set of views. You can name the question without choosing diagram types.
Supported views include:

- Use context maps to explain meaning boundaries and relationships between domain models.
- Use conceptual class models to explain business concepts, relationships, and relevant cardinalities.
- Use activity diagrams to explain business flows, decisions, handoffs, and unsuccessful outcomes.
- Use DMN-style decision tables to examine conditions, results, overlapping rules, and missing cases.
  DMN is short for Decision Model and Notation.
- Use timelines to explain event order, deadlines, intervals, and material time boundaries.
- Use responsibility matrices to explain who acts, supplies information, or makes a decision.

The domain guidance covers scoped meanings, context relationships and candidate consistency
boundaries. Context analysis examines translation, decision ownership and information restrictions.
See the [domain guidance](skills/define-change/references/domain-meaning.md) and
[modelling guidance](skills/define-change/references/models.md).

For architecture and technical models, use `design-solution`. It supports C4 system context,
component, conceptual class, entity-relationship, sequence, activity, and state models. The skill
chooses useful views and routine notation itself. Architecture documents created or revised with
the skill include a C4 system context diagram; other models are discretionary when they explain
an important relationship better than prose. Preflight does not prescribe an architecture style
or pattern. Choose boundaries and mechanisms against your requirements and constraints.
See the [architecture](skills/design-solution/references/architecture.md) and
[design modelling](skills/design-solution/references/models.md) guidance.

Both skills support editable Mermaid diagrams. Conceptual class diagrams and activity flowcharts
can explain business meaning. Technical views also support Mermaid C4, entity-relationship,
sequence, and state diagrams. Decision tables, responsibility matrices, and precise time constraints
can use Markdown. Follow the repository's supported formats and viewer capabilities.

For model selection by the skill, try:

> $define-change Model these requirements using appropriate diagrams and tables.

> $design-solution Model this design using appropriate Mermaid diagrams.

Name a specific model when you require that output, such as "Add a sequence diagram in Mermaid."
Explicitly requested models are deliverables. A general review does not request a model bundle.
See the [define-change model guide](skills/define-change/README.md#supported-models-and-mermaid-diagrams)
and [design-solution model guide](skills/design-solution/README.md#supported-models-and-mermaid-diagrams).

Keep editable model source. Check meaning separately from diagram syntax, rendering, and
viewer compatibility. Rendering depends on available tools; the agent must report checks it could
not complete. A diagram that renders successfully can still express the wrong rule.

## Assess the outputs before relying on them

Read the result against your original objective and sources. Check that you can explain:

- What the result means for the people who use the system and whether it solves the intended problem.
- Which rules and decisions are accepted, proposed, inferred, or still unresolved.
- Which assumptions, alternatives, and consequential choices affect the result.
- What was produced, what was actually checked, and what the available evidence establishes.
- What remains to be decided or verified, what can proceed, and what the next person or agent needs.

If a term, rule, diagram, or conclusion is unclear, ask for an explanation with a concrete example.
Do not accept an artifact merely because its format is valid or its prose sounds confident.
Passing selected checks does not establish every requirement or error path.

Use the shared [principles](shared/principles.md), [artifact conventions](shared/artifacts.md), and
[writing guidance](shared/writing.md) to understand the expected distinctions. Follow repository
conventions where they already govern the work.

## Install the skills

Use Python 3.10 or later for installation. The installer uses the standard library.

For a project installation, run this command from the Preflight checkout. The destination must be
the root of a Git worktree:

```sh
python3 deploy.py install --repo /path/to/project \
	define-change design-solution
```

For a user installation, run:

```sh
python3 deploy.py install --user \
	define-change design-solution
```

`--user` creates links in `~/.agents/skills`. Keep the Preflight checkout in place for those links.

If your agent discovers another skill directory, choose that destination explicitly. For example:

```sh
python3 deploy.py install --target "$HOME/.claude/skills" \
	define-change design-solution
```

Project installations and other explicit targets receive self-contained snapshots of the skills,
shared references, and model presets. Explicit targets matching `~/.agents/skills` or
`$CODEX_HOME/skills` also use links. If `CODEX_HOME` is unset, the latter directory is `~/.codex/skills`.
Select fewer skill names if you need only part of Preflight.

Preflight requires no external skill package or specific search provider. It prepares requirements,
domain models, and technical designs; it does not implement changes. Pass its outputs to your chosen
implementation workflow using the [handoff guidance](shared/execution-handoff.md).

Keep implementation, verification, commit, pull-request, merge, and deployment procedures in your
repository or execution workflow. Invoking Preflight does not install or configure that workflow.

## Inspect, update, or remove an installation

To inspect a project's skill entries, run:

```sh
python3 skill_install.py list --target /path/to/project/.agents/skills
```

For your user installation, use `python3 skill_install.py list --user`.

To update snapshots or convert an existing physical user copy to a source link, use `reinstall`
with the same destination and selected names:

```sh
python3 deploy.py reinstall --repo /path/to/project \
	define-change design-solution
```

To remove selected skills, use:

```sh
python3 deploy.py uninstall --repo /path/to/project \
	define-change design-solution
```

Substitute `--user` or `--target /path/to/skills` for other destinations. Existing physical user copies are backed
up before conversion to links. Snapshot updates and removal preserve managed copies in backups.
For snapshot recovery, use `restore --backup <id>` with one skill name. Read
`python3 deploy.py --help` for the exact options. Unrelated skills and files are preserved.

## Configure models when you need delegation

For delegated preparation or independent review, follow the
[model routing guide](shared/model-selection.md). Configure model selectors supported by your
runtime, inspect the proposed assignments, and apply only the configuration you intend to use.
Explicit user assignments take precedence.

The model helpers require PyYAML. Use an existing environment with that dependency or the locked
development environment. To inspect the configuration commands in the locked environment, run
`uv run --locked python shared/configure_models.py --help`. Resolving an assignment does not launch
an agent or switch the current session's model. Serial work can stay in the current session.

## Consult the underlying methods

Use these freely accessible sources for the practices reflected in Preflight. They support the
methodology. They do not establish that Preflight fully implements each method or standard.

- Read [IIBA's Business Analysis Standard, free PDF](https://www.iiba.org/globalassets/business-analysis-resources/the-business-analysis-standard/files/the-business-analysis-standard.pdf)
  for requirements modelling, verification, validation, traceability, and change assessment.
- Read [SEBoK's Stakeholder Needs Definition](https://sebokwiki.org/wiki/Stakeholder_Needs_Definition)
  for establishing needs and using them as the basis for requirements and validation.
- Read [Eric Evans's DDD Reference, free PDF](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
  for domain models, ubiquitous language, bounded contexts, context maps, aggregates, and invariants.
- Read [Rozanski and Woods on viewpoints](https://www.viewpoints-and-perspectives.info/home/viewpoints/)
  and [perspectives](https://www.viewpoints-and-perspectives.info/home/perspectives/)
  for architectural views and quality concerns that span those views.
- Read [CMU SEI's ATAM report, free PDF](https://www.sei.cmu.edu/documents/629/2000_005_001_13706.pdf)
  for scenario-based architectural evaluation, quality attributes, risks, and tradeoffs.
- Use [Simon Brown's C4 model](https://c4model.com/) to understand the architecture views and
  [Michael Nygard's original ADR article](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  for decision context, consequences, and history.
- Use [Cucumber's Example Mapping guidance](https://cucumber.io/docs/bdd/example-mapping/) to
  distinguish rules, examples, and open questions. Consult the [OMG UML specification](https://www.omg.org/spec/UML/2.5.1)
  and [DMN specification](https://www.omg.org/spec/DMN/1.5/About-DMN) for the modelling notations.

## Check the package when you contribute

Run these checks from the Preflight checkout. Development checks use uv, mypy, Ruff, and PyYAML:

```sh
uv run --locked mypy --config-file pyproject.toml
uv run --locked ruff check --config pyproject.toml .
uv run --locked ruff format --check --config pyproject.toml .
uv run --locked python -m unittest discover -s tests -v
```

Package checks use disposable targets. Before changing real installations, exercise installation
and configuration commands against a temporary target and a disposable project. Package checks
establish the properties they check. They do not establish the correctness of generated designs or
an agent's adherence to the instructions.

## License

MIT. See [LICENSE](LICENSE).
