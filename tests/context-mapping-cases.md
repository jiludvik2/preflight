# Context mapping exercises

Use supplied sources and bounded native-agent requests. Establish expected outcomes from those
sources before running actors. Withhold assessor expectations from actors and retain actual inputs,
loaded guidance, output and limitations. These cases are verification guidance, not passing evidence.

## Meaning and information boundaries

Use this accepted scenario:

> Booking Operations defines a cancelled booking as a booking no longer taking place. Billing
> defines a cancelled charge as a charge reversed before settlement. A booking cancellation does
> not establish that a charge was reversed. Billing owns payment state. Refund Policy owns the
> refund decision using a supplied eligibility result. It may receive that result and a booking
> reference, but must not receive the underlying clinical reason. Booking Operations supplies the
> result without owning the refund decision. Billing and Refund Policy must participate when the
> supplied eligibility meanings change.

Ask for contextual analysis in a proposed domain definition, with no map request. Check that the
actor preserves the distinct cancellation meanings, fact and decision ownership, information limit
and participation obligations. During Draft or substantive Revise, include a context map when those
material meaning boundaries and relationships need it; Review and Validate remain read-only.

Then explicitly request a context-map diagram for the same concern. Check that it includes editable
source, useful context scopes and labelled relationships. It must not imply that booking cancellation
proves reversed payment, send clinical details across the boundary, or turn contexts into services.
Check semantic fidelity separately from exact diagram syntax, visual rendering and viewer support.
An unavailable renderer limits rendering evidence, not established domain meaning.

## Revealing cases and valid controls

| Supplied source and request | Expected outcome |
| --- | --- |
| A source translates both unpaid and reversed payment into one `closed` value, but the consumer must distinguish them. Review the translation. | Identify the lost distinction and affected consumer decision; do not invent missing source facts or declare the mapping sufficient. |
| The consumer needs a clinical reason to decide, but the accepted source prohibits its receipt. | Identify the incompatible decision inputs or missing authorized decision; do not add the prohibited information to complete the model. |
| Two teams use different aliases for the same accepted model and rules. Assess whether separate contexts are needed. | Do not infer a new bounded context merely from team or naming differences. |
| A context supplies facts but no source assigns ownership of a derived decision. Draw the affected map. | Identify the consequential missing decision and preserve the existing dependent-model gate; do not assign ownership from the data flow. |
| Suggest where context mapping would help this domain definition. | Return recommendations without generating a map. |
| Review only the translation between two accepted contexts. | Keep the assessment read-only and scoped; do not redraw the whole domain or accept changes. |
| Revise an accepted contextual agreement affecting one consumer. | Preserve the accepted baseline, identify affected meanings and consumers, and apply existing proposed-change and independent-review rules. |
| Design a solution using the established context relationships. | Preserve semantic and information constraints while assessing technical choices; do not assume one service, schema or deployment per context. |

## Package and comparison checks

Use each pack's existing required checks and skill metadata/reference validation. Install only into
a disposable target and confirm the installed entrypoint reaches the context-analysis and context-map
guidance, including links between semantic, modelling and shared references. Preserve old heading
anchors and verify that shipping model presets and helper implementations are unchanged.

For any quality-improvement claim, use a separate actor on the prior skill with the same source and
request. Compare concrete semantic outcomes, not report length or terminology counts. A bounded
exercise does not establish general reliability. Do not create a permanent evaluation framework.
