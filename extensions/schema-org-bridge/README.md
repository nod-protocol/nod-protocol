# Schema.org Bridge Extension

**Manifest key:** `extensions["ai.opennod.schema-org-extension"]`
**Schema:** [`v0.1.json`](./v0.1.json) — `https://opennod.ai/schema/extensions/schema-org-bridge/v0.1.json`
**Status:** v0.1 (meta-schema only). Per-subtype JSON Schemas are not yet shipped; consumers validate the `properties` payload themselves.

---

## Purpose

Lets a merchant declare which Schema.org `LocalBusiness` subtype applies
to them, and supply that subtype's industry-specific properties as a
structured payload. This is the bridge between the nod core schema (which
is industry-agnostic) and the rich per-industry vocabulary Schema.org
already maintains.

The protocol's stance on Schema.org is **adopt, don't reinvent**. A
restaurant has `servesCuisine`, `acceptsReservations`, `hasMenu`,
`priceRange`; a medical business has `medicalSpecialty` and
`healthPlanNetworkId`; a lodging business has `checkinTime`,
`checkoutTime`, `numberOfRooms`. We use those property names as-is.

## What v0.1 does and does not do

**Does:**
- Defines `schema_org_type` (the LocalBusiness subtype name)
- Reserves a `properties` object for the subtype's industry-specific fields
- Constrains `schema_org_type` to a PascalCase string matching Schema.org's
  type-name convention

**Does not:**
- Validate that `schema_org_type` is actually a real Schema.org type
  (consumers may check against [the canonical subtype list](https://schema.org/LocalBusiness#subtypes))
- Validate that fields inside `properties` match the chosen subtype's
  expected properties (consumers do this against Schema.org's vocabulary)

A future revision (`v0.2` of this extension or later) may ship per-subtype
JSON Schemas under `extensions/schema-org-bridge/types/<TypeName>.json` so
that strict validators can check field shapes automatically. The decision
on whether to ship those schemas, and how to keep them in sync with
Schema.org's evolution, is deferred.

## Fields

### `schema_org_type` *(string, required)*

Name of a Schema.org type that is a subtype of `LocalBusiness` (directly
or transitively). Examples of common direct subtypes:

`AnimalShelter`, `AutomotiveBusiness`, `ChildCare`, `Dentist`,
`DryCleaningOrLaundry`, `EmergencyService`, `EmploymentAgency`,
`EntertainmentBusiness`, `FinancialService`, `FoodEstablishment`,
`GovernmentOffice`, `HealthAndBeautyBusiness`, `HomeAndConstructionBusiness`,
`LegalService`, `Library`, `LodgingBusiness`, `MedicalBusiness`,
`ProfessionalService`, `RadioStation`, `RealEstateAgent`, `RecyclingCenter`,
`SelfStorage`, `ShoppingCenter`, `SportsActivityLocation`, `Store`,
`TelevisionStation`, `TouristInformationCenter`, `TravelAgency`.

Transitive subtypes are also valid — e.g. `Restaurant` (under
`FoodEstablishment`), `Hotel` (under `LodgingBusiness`), `Hospital` (under
`MedicalBusiness`), `BookStore` (under `Store`).

Use the most specific subtype that accurately applies. A pizza restaurant
should be `Restaurant`, not `FoodEstablishment`.

### `schema_org_version` *(string, optional)*

The Schema.org vocabulary version this declaration was authored against
(e.g. `"28.0"`). Informational — Schema.org does not version property
shapes strictly, but recording the version helps debug field availability.

### `context` *(string, default `"https://schema.org"`)*

JSON-LD `@context` URL. Override only if using a Schema.org extension
vocabulary.

### `properties` *(object, required)*

The merchant's industry-specific Schema.org properties for the declared
subtype. Property names follow Schema.org conventions (camelCase).

## Example: Restaurant

```json
{
  "extensions": {
    "ai.opennod.schema-org-extension": {
      "schema_org_type": "Restaurant",
      "properties": {
        "servesCuisine": ["Italian", "Pizza"],
        "acceptsReservations": "https://example.com/reserve",
        "priceRange": "$$",
        "hasMenu": "https://example.com/menu.pdf",
        "starRating": { "@type": "Rating", "ratingValue": "4.5" }
      }
    }
  }
}
```

## Example: MedicalBusiness

```json
{
  "extensions": {
    "ai.opennod.schema-org-extension": {
      "schema_org_type": "MedicalClinic",
      "schema_org_version": "28.0",
      "properties": {
        "medicalSpecialty": ["Pediatric", "Dermatology"],
        "healthPlanNetworkId": ["BCBS-IL-PPO"],
        "isAcceptingNewPatients": true
      }
    }
  }
}
```

## Why a bridge instead of inlining Schema.org fields directly?

Two reasons:

1. **Namespace hygiene.** A merchant manifest can grow large; isolating
   industry-specific Schema.org properties under one extension key keeps
   the core schema flat and predictable.
2. **Validation pluggability.** Future strict validators can dispatch on
   `schema_org_type` to apply the right per-subtype schema. Inlining at
   the core level would couple the core schema to Schema.org's evolution.
