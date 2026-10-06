# Relationship Model

The relationship pass uses constrained predicate families. This prevents the graph from degenerating into vague `related_to` edges and keeps different mechanisms distinct.

## structural

`part_of` · `contains` · `belongs_to` · `member_of` · `branch_of` · `subordinate_to` · `superior_to` · `reports_to` · `governs` · `administers` · `represents` · `owns` · `controls` · `occupies` · `inhabits` · `located_in` · `headquartered_in` · `originates_in` · `operates_in` · `claims` · `borders` · `overlaps` · `encloses` · `surrounds` · `connects` · `separates`

## political

`rules` · `governs` · `recognizes` · `supports` · `opposes` · `challenges` · `legitimizes` · `delegitimizes` · `appoints` · `elects` · `inherits_from` · `succeeds` · `vassal_of` · `overlord_of` · `tributary_of` · `protector_of` · `client_of` · `patron_of` · `dependent_on` · `influences` · `lobbies` · `pressures` · `coerces` · `sanctions` · `subsidizes` · `regulates`

## diplomatic

`allied_with` · `at_war_with` · `neutral_toward` · `recognizes` · `does_not_recognize` · `treaty_with` · `guarantees` · `protects` · `mediates_between` · `negotiates_with` · `embargoes` · `sanctions` · `trades_with` · `has_embassy_in` · `claims_against` · `disputes_with` · `competes_with` · `balances_against` · `appeases` · `deters`

## economic

`produces` · `consumes` · `imports` · `exports` · `supplies` · `buys_from` · `sells_to` · `finances` · `invests_in` · `lends_to` · `borrows_from` · `insures` · `employs` · `works_for` · `owns` · `leases` · `rents` · `taxes` · `subsidizes` · `monopolizes` · `competes_with` · `depends_on` · `substitutes_for` · `complements` · `processes` · `distributes` · `warehouses` · `transports` · `retails` · `wholesales`

## resource

`extracts` · `harvests` · `mines` · `grows` · `raises` · `hunts` · `fishes` · `processes` · `refines` · `stores` · `consumes` · `depletes` · `protects` · `contaminates` · `controls_access_to` · `depends_on` · `competes_for`

## military

`commands` · `serves_under` · `garrisons` · `defends` · `attacks` · `besieges` · `occupies` · `raids` · `patrols` · `blockades` · `escorts` · `supplies` · `reinforces` · `recruits_from` · `trains` · `equips` · `funds` · `fortifies` · `threatens` · `deters`

## criminal

`smuggles_for` · `bribes` · `blackmails` · `extorts` · `robs` · `steals_from` · `fences_for` · `protects` · `corrupts` · `infiltrates` · `launders_for` · `assassinates` · `traffics` · `supplies_illegally` · `controls_racket` · `pays_protection_to`

## social

`parent_of` · `child_of` · `sibling_of` · `spouse_of` · `lover_of` · `friend_of` · `rival_of` · `mentor_of` · `student_of` · `master_of` · `apprentice_of` · `patron_of` · `client_of` · `neighbor_of` · `clan_member_of` · `house_member_of` · `servant_of` · `employer_of` · `owes_favor_to` · `trusts` · `distrusts` · `admires` · `resents` · `fears`

## religious

`worships` · `serves` · `is_clergy_of` · `opposes_faith` · `considers_heretical` · `consecrates` · `controls_temple` · `pilgrimages_to` · `receives_revelation_from` · `chosen_by` · `cursed_by` · `blessed_by`

## magical

`enchants` · `created_by` · `attuned_to` · `bound_to` · `summoned_by` · `controls` · `wards_against` · `counters` · `channels` · `draws_power_from` · `corrupted_by` · `sealed_by` · `opens_portal_to` · `teleports_to` · `amplifies` · `suppresses`

## spatial

`north_of` · `south_of` · `east_of` · `west_of` · `upstream_of` · `downstream_of` · `coastal_to` · `adjacent_to` · `inside` · `outside` · `above` · `below` · `near` · `far_from` · `connected_by` · `accessible_via` · `separated_by` · `overlooks` · `dominates_route_to`

## temporal

`before` · `after` · `during` · `overlaps_with` · `begins` · `ends` · `causes` · `follows` · `precedes` · `continues` · `interrupts` · `replaces` · `revives` · `recurs` · `annually` · `seasonally`

## information

`knows` · `believes` · `suspects` · `does_not_know` · `hides_from` · `reveals_to` · `lies_to` · `informs` · `warns` · `misleads` · `spies_on` · `reports_to` · `records` · `forgets` · `remembers` · `censors` · `publishes`

## causal

`causes` · `contributes_to` · `enables` · `prevents` · `inhibits` · `accelerates` · `slows` · `amplifies` · `reduces` · `triggers` · `requires` · `results_in` · `creates_pressure_for` · `creates_incentive_for` · `destabilizes` · `stabilizes` · `reinforces` · `undermines`

## dependency

`depends_on` · `critically_depends_on` · `partially_depends_on` · `relies_on` · `requires` · `can_substitute` · `cannot_substitute` · `is_vulnerable_to_loss_of` · `has_backup_for`

## legal

`authorizes` · `prohibits` · `mandates` · `regulates` · `licenses` · `grants_right_to` · `revokes_right_of` · `adjudicates` · `enforces_against` · `appeals_to` · `bound_by` · `exempts` · `has_jurisdiction_over`

## power

`has_authority_over` · `influences` · `controls` · `can_veto` · `can_coerce` · `can_reward` · `can_punish` · `can_mobilize` · `can_withhold` · `can_legitimize` · `derives_legitimacy_from`

## capability

`capable_of` · `incapable_of` · `capacity_limit` · `projects_power_into` · `reaches` · `can_supply` · `can_defend` · `can_disrupt`

## flow

`flows_to` · `flows_from` · `routed_through` · `originates_at` · `terminates_at` · `passes_through` · `diverted_to` · `bottlenecked_by` · `distributed_by`

## logistical

`supplied_by` · `transported_via` · `stored_at` · `provisioned_by` · `stages_at` · `resupplied_at` · `depends_on_route` · `rerouted_via`

## infrastructure

`served_by` · `connected_to` · `powered_by` · `supplied_water_by` · `drains_to` · `protected_by` · `maintained_by` · `constrained_by_capacity_of`

## ecological

`preys_on` · `eaten_by` · `pollinates` · `parasitizes` · `symbiotic_with` · `competes_for` · `inhabits` · `migrates_through` · `depends_on_habitat` · `degrades_habitat_of`

## technological

`invented_by` · `developed_by` · `manufactured_by` · `maintained_by` · `requires_technology` · `enables_technology` · `derived_from` · `compatible_with` · `supersedes` · `disseminated_to`

## epistemic

`supports_claim` · `contradicts_claim` · `corroborates` · `disputes` · `inferred_from` · `assumes` · `uncertain_about` · `source_for`

## provenance

`sourced_from` · `quoted_in` · `recorded_in` · `corrected_by` · `superseded_by` · `derived_from_source` · `attested_by` · `first_appears_in`

## cultural

`speaks` · `uses_script` · `practices` · `observes` · `celebrates` · `taboo_against` · `influenced_by_culture` · `adopts_custom_from`

## biological

`transmits_disease_to` · `infected_by` · `treats` · `heals` · `poisons` · `immune_to` · `vulnerable_to`

## interaction

`affects` · `externalizes_cost_to` · `creates_spillover_for` · `buffers` · `mediates_effect_of` · `couples_with`

## Extraction rules

- Only emit a typed relationship when the source supports it.
- Do not convert an inference into a source-grounded relation.
- Preserve directionality. `A supplies B` is not equivalent to `B supplies A`.
- Prefer mechanism-specific predicates over generic influence when the mechanism is known.
- Use temporal validity and perspective fields when a relationship is era-bound or viewpoint-bound.
- Keep source provenance on every record so conflicting editions can coexist until review.
