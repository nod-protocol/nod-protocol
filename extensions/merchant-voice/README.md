# Merchant-Voice Extension

**Manifest key:** `extensions["ai.opennod.merchant-voice"]`
**Schema:** [`v0.1.json`](./v0.1.json) — `https://opennod.ai/schema/extensions/merchant-voice/v0.1.json`
**Status:** v0.1, stable.

---

## Purpose

Free-text narrative fields a merchant uses to express positioning, story,
and specialties. Distinct from structured business metadata (which is in
core) and from agent-commerce mechanics (which is in the agent-commerce
extension).

Agents may surface these to humans verbatim, use them to inform
recommendations, or both. The protocol does not constrain how consumers
interpret merchant-voice content.

## Fields

### `positioning_statement` *(string, max 280 chars)*

One-sentence statement of how the merchant positions itself. The 280-char
cap is a forcing function for concision — longer claims belong in `story`.

### `ideal_customer` *(string, max 500 chars)*

Plain-language description of the customer the merchant is built for.
Used by agents during recommendation tasks. Merchants should describe
the customer they actually serve, not an aspirational one.

### `story` *(string, max 4000 chars)*

Longer-form narrative: founding context, what makes this merchant
different, why it exists. Optional; merchants who don't have a story
they want surfaced should omit it rather than write filler.

### `specialties` *(array of short strings)*

Things this merchant is unusually good at, as short noun phrases.
Examples: *"wood-fired Neapolitan pizza"*, *"IRS audit defense for
small businesses"*. Avoid generic claims that any competitor would
also list — generic specialties dilute recommendation usefulness.

### `accommodations` *(array of short strings)*

Customer accommodations the merchant explicitly offers. Examples:
*"wheelchair-accessible entrance and restroom"*, *"gluten-free
kitchen"*, *"after-hours appointments by request"*, *"on-site
interpreter for ASL"*.

This is for capabilities a customer might filter on — not a marketing
list. If the accommodation is an aspiration rather than a reliable
offering, omit it.

## Example

```json
{
  "extensions": {
    "ai.opennod.merchant-voice": {
      "positioning_statement": "Naples-style pizza for diners who notice the difference between 60-second and 90-second bakes.",
      "ideal_customer": "Pizza enthusiasts and food professionals visiting from out of town. We are not the spot for a kid's birthday party.",
      "story": "Opened in 2019 by a husband-and-wife team who spent four years apprenticing in Naples. Our oven is a Stefano Ferrara forno; flour is Caputo 00, imported direct.",
      "specialties": [
        "wood-fired Neapolitan pizza",
        "natural-leavened dough (48-hour cold ferment)",
        "anchovies cured in-house"
      ],
      "accommodations": [
        "gluten-free dough available with 24h notice",
        "wheelchair-accessible entrance and restroom",
        "highchairs available"
      ]
    }
  }
}
```
