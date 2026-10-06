# Ontology Catalog

Registry version: **2026-10-06.2**

- Named source/domain/system extractors: **419**
- Operational extractors including virtual routing/inference layers: **471**
- Relationship families: **28**

The catalog is deliberately redundant at the lens level. Extraction records are normalized later; the router should prefer relevant packs instead of running every lens over every chunk.

## Entity layer

### 1. Core entity extractors

- **general**: people; places; organizations; objects; creatures; concepts; events; documents; titles; terminology; aliases; relationships
- **personal**: names; aliases; age; ancestry; occupation; rank; affiliation; residence; personality; goals; fears; beliefs; possessions; relationships; history; reputation; capabilities
- **organizational**: organizations; leadership; hierarchy; membership; branches; headquarters; resources; responsibilities; procedures; history; alliances; enemies; internal divisions
- **factional**: factions; ideology; objectives; leadership; members; territory; resources; methods; allies; enemies; reputation; internal factions
- **institutional**: institutions; mandates; authority; jurisdiction; procedures; resources; personnel; traditions; legitimacy; dependencies
- **object**: objects; tools; weapons; documents; artifacts; vehicles; materials; owners; makers; uses; values; provenance
- **creature**: species; monsters; animals; populations; habitats; behavior; diet; reproduction; intelligence; abilities; relationships
- **conceptual**: ideas; doctrines; theories; philosophies; beliefs; technical concepts; magical concepts; social concepts

## Domain layer

### 2. Economic and commercial domains

- **economic**: production; consumption; trade; scarcity; prices; wealth; resources; industries; labor; capital; economic dependencies
- **commercial**: commerce; merchants; contracts; marketplaces; sales; distribution; wholesalers; retailers; commercial customs
- **mercantile**: merchant houses; trading companies; caravans; shipping; commodity trade; merchant networks; monopolies; intermediaries
- **financial**: credit; lending; debt; interest; banking; investment; collateral; insurance; defaults; financial institutions
- **monetary**: currencies; coinage; exchange rates; minting; debasement; money supply; currency zones; counterfeit currency
- **fiscal**: taxation; duties; tariffs; tolls; tribute; government revenue; expenditure; tax farming; exemptions; public debt
- **industrial**: industries; workshops; factories; production centers; inputs; outputs; labor; capacity; specialization
- **manufacturing**: production methods; workshops; tools; labor; inputs; outputs; quality; scale; specialization; costs
- **craft**: crafts; artisans; guilds; apprentices; techniques; tools; materials; regional specialities
- **agricultural**: crops; livestock; farming; fisheries; forestry; land ownership; yields; irrigation; labor; seasonality
- **pastoral**: herding; grazing; livestock; migration; pasture rights; seasonal movement; animal products
- **extractive**: mining; quarrying; logging; fishing; harvesting; resource deposits; concessions; depletion
- **commodity**: commodities; sources; destinations; prices; volumes; substitutes; strategic value; seasonality
- **market**: markets; buyers; sellers; market days; prices; competition; monopolies; market access; regulation
- **labor**: occupations; wages; labor supply; guilds; slavery; serfdom; apprenticeships; unemployment; specialization
- **property**: ownership; tenancy; leases; estates; inheritance; commons; rents; mortgages; confiscation
- **wealth**: wealth distribution; elites; poverty; assets; income; luxury consumption; inequality; economic mobility
- **supply-chain**: sources; producers; processors; warehouses; transport; distributors; markets; consumers; chokepoints
- **logistical**: transport; warehousing; provisioning; distribution; capacity; lead times; bottlenecks; redundancy
- **scarcity**: scarce resources; causes; substitutes; prices; rationing; political consequences; social consequences
- **consumption**: food; clothing; fuel; luxury goods; household goods; consumption patterns; class differences
- **investment**: capital allocation; investors; projects; returns; risk; ownership; financing structures
- **insurance**: risk pooling; insurers; premiums; covered risks; maritime insurance; magical insurance; indemnities
- **entrepreneurial**: new ventures; innovators; merchant adventurers; commercial opportunities; barriers; financing
- **informal-economy**: barter; household production; informal labor; unregistered trade; favors; reciprocal exchange

### 3. Governmental and political domains

- **governmental**: government; rulers; ministries; councils; offices; administration; jurisdiction; public authority
- **political**: power blocs; factions; ideology; influence; legitimacy; political interests; competition
- **administrative**: administration; districts; officials; procedures; records; permits; taxation; implementation
- **bureaucratic**: bureaucracies; offices; paperwork; chains of command; appointment; institutional inertia; administrative capacity
- **constitutional**: constitutional order; succession; division of powers; rights; privileges; institutional limits
- **monarchical**: monarchs; dynasties; succession; royal households; court politics; royal prerogatives
- **aristocratic**: nobility; titles; estates; privileges; houses; inheritance; patronage; feuds
- **republican**: councils; voting; magistrates; citizenship; representation; civic institutions
- **municipal**: city government; mayors; councils; wards; local taxation; public works; policing
- **provincial**: regional administration; governors; provinces; local elites; center-periphery relations
- **imperial**: empire; provinces; tribute; colonial administration; imperial ideology; frontier control
- **feudal**: lords; vassals; fiefs; obligations; homage; tenure; military service; feudal hierarchy
- **patrimonial**: personal rule; household administration; patronage; office holding; gift exchange
- **governance**: capacity; legitimacy; implementation; public goods; corruption; reach; institutional effectiveness
- **policy**: policies; goals; instruments; target groups; implementation; effects; unintended consequences

### 4. Legal and juridical domains

- **legal**: laws; crimes; contracts; rights; obligations; legal institutions; jurisdiction
- **juridical**: courts; judges; trials; rulings; legal procedure; precedent; appeals; enforcement
- **criminal-law**: crimes; punishments; prosecution; detention; evidence; criminal procedure
- **civil-law**: contracts; property; inheritance; debts; disputes; compensation
- **commercial-law**: merchant law; shipping law; contracts; bankruptcy; guild regulation; trade disputes
- **maritime-law**: salvage; piracy; ship ownership; cargo claims; harbor law; privateering; wreck law
- **customary-law**: traditions; customary rights; unwritten law; local practice; customary authority
- **canonical-law**: religious law; clerical courts; doctrinal offenses; marriage; burial; temple jurisdiction
- **magical-law**: restricted magic; spell licensing; forbidden spells; artifact possession; magical crimes
- **property-law**: ownership; tenancy; inheritance; easements; land claims; seizure
- **jurisdictional**: territorial jurisdiction; institutional jurisdiction; overlapping authority; legal conflicts

### 5. Diplomatic and geopolitical domains

- **diplomatic**: treaties; alliances; ambassadors; negotiations; recognition; disputes; diplomatic customs
- **geopolitical**: strategic geography; regional powers; spheres of influence; chokepoints; buffer states; geopolitical competition
- **international-relations**: alliances; rivalries; balance of power; institutions; interdependence; deterrence
- **treaty**: treaties; signatories; obligations; duration; violations; enforcement; consequences
- **envoy**: ambassadors; emissaries; missions; diplomatic immunity; negotiating mandates
- **tribute**: tribute; suzerainty; protection payments; symbolic submission; tributary relationships
- **vassalage**: overlords; vassals; obligations; autonomy; military support; taxation
- **border**: borders; contested territory; checkpoints; cross-border movement; border communities
- **colonial**: colonies; settlers; indigenous populations; resource extraction; administration; resistance
- **hegemonic**: regional dominance; dependent states; coercion; prestige; economic leverage

### 6. Martial and military domains

- **martial**: armed forces; warfare; soldiers; equipment; fortifications; command; readiness
- **military**: army structure; units; command; recruitment; doctrine; logistics; campaigns
- **strategic**: war aims; theaters; strategic resources; alliances; chokepoints; grand strategy
- **operational**: campaigns; maneuver; supply; concentration; operational objectives
- **tactical**: formations; battlefield methods; weapons; terrain use; unit tactics
- **naval**: navies; fleets; warships; naval bases; doctrine; blockades; convoy protection
- **maritime-military**: privateers; marines; amphibious warfare; coastal defenses; naval logistics
- **siege**: fortifications; siege engines; supplies; siege tactics; defenses; breaches
- **fortification**: walls; towers; castles; forts; bastions; garrisons; defensive depth
- **logistics-military**: supply lines; depots; food; ammunition; transport; remounts; replacement troops
- **recruitment**: levies; volunteers; conscription; mercenaries; recruitment regions; incentives
- **mercenary**: mercenary companies; contracts; employers; loyalty; rates; reputation
- **militia**: local militias; musters; equipment; training; obligations
- **intelligence-military**: scouting; reconnaissance; spies; signals; military intelligence
- **doctrinal**: military doctrines; preferred tactics; command philosophies; institutional traditions
- **readiness**: mobilization; equipment condition; reserves; training; response times
- **veteran**: veteran populations; pensions; mercenary migration; political influence; martial culture

### 7. Security and intelligence domains

- **security**: guards; policing; border control; protective measures; threats; security institutions
- **policing**: watchmen; patrols; arrests; investigations; jurisdiction; response capacity
- **intelligence**: spies; networks; informants; intelligence agencies; collection; analysis; covert operations
- **counterintelligence**: spy detection; secrecy; infiltration; double agents; security procedures
- **surveillance**: observation; informants; magical surveillance; records; tracking
- **espionage**: agents; missions; targets; methods; handlers; secrets; compromised networks
- **covert-action**: sabotage; assassinations; subversion; proxy actors; deniable operations
- **emergency**: disasters; emergency institutions; response plans; mobilization; evacuation

### 8. Illicit and criminal domains

- **illicit**: crime; contraband; smuggling; corruption; illegal services; black markets
- **criminal**: crimes; criminals; criminal organizations; methods; territories; victims
- **underworld**: gangs; thieves; fences; smugglers; assassins; safehouses; criminal hierarchies
- **smuggling**: contraband; routes; smugglers; corrupt officials; concealment; border crossings
- **piratical**: pirates; bases; targets; ships; routes; fences; protection arrangements
- **corruption**: bribes; patronage; embezzlement; favoritism; captured institutions; corrupt networks
- **black-market**: illegal goods; prices; suppliers; buyers; meeting places; enforcement risks
- **organized-crime**: syndicates; territories; leadership; rackets; alliances; conflicts
- **fraud**: forgery; scams; false contracts; counterfeit goods; identity fraud; financial fraud
- **assassination**: assassins; contracts; targets; methods; intermediaries; political consequences

### 9. Sociological and anthropological domains

- **sociological**: classes; institutions; status; norms; social networks; inequality; mobility
- **anthropological**: culture; kinship; ritual; material culture; social organization; worldview
- **ethnographic**: daily practices; local customs; identity; food; clothing; speech; ritual behavior
- **demographic**: population; age; ancestry; sex; household; migration; fertility; mortality
- **kinship**: families; clans; marriages; descent; inheritance; adoption; obligations
- **class**: elites; middle strata; laborers; peasants; slaves; status groups
- **status**: prestige; titles; social rank; honor; reputation; stigma
- **mobility**: social mobility; geographic mobility; career mobility; class transitions
- **inequality**: wealth inequality; political inequality; legal privilege; access disparities
- **community**: neighborhoods; villages; associations; mutual aid; local identity
- **diaspora**: diasporic groups; migration; homelands; trade networks; identity; remittances
- **migration**: immigration; emigration; refugees; seasonal migration; causes; destinations
- **refugee**: displaced populations; camps; destinations; causes; political pressures
- **minority**: minority groups; rights; discrimination; autonomy; cultural preservation
- **identity**: regional identity; religious identity; ethnic identity; occupational identity; civic identity

### 10. Cultural and symbolic domains

- **cultural**: customs; values; traditions; arts; symbols; norms; regional identity
- **semiotic**: symbols; signs; colors; heraldry; ritual meanings; coded meanings
- **linguistic**: languages; dialects; scripts; literacy; loanwords; multilingualism
- **philological**: word origins; historical language; old texts; translation; textual variants
- **literary**: books; poetry; epics; genres; authors; narrative traditions
- **artistic**: painting; sculpture; decoration; patronage; artistic schools
- **musical**: music; instruments; performers; songs; musical traditions
- **theatrical**: theater; performers; venues; genres; audiences
- **culinary**: food; recipes; ingredients; cuisine; dining customs; regional dishes
- **fashion**: clothing; hairstyles; jewelry; status markers; regional fashion
- **heraldic**: coats of arms; badges; colors; symbols; lineage marks
- **ceremonial**: ceremonies; processions; coronations; public rituals; civic rituals
- **festive**: festivals; holidays; fairs; seasonal celebrations; competitions
- **funerary**: burial; cremation; tombs; mourning; funerary rites
- **marital**: marriage customs; dowries; contracts; alliances; divorce; inheritance
- **hospitality**: guest-right; hosting; food; gift exchange; etiquette
- **taboo**: prohibitions; social taboos; sacred taboos; pollution; forbidden behavior

### 11. Psychological and behavioral domains

- **psychological**: motivation; fear; desire; trauma; personality; perception; cognition
- **motivational**: goals; incentives; fears; ambitions; loyalties; pressures
- **behavioral**: habits; routines; decision patterns; social behavior; reactions
- **emotional**: anger; grief; love; shame; fear; pride; resentment
- **reputational**: reputation; rumors; prestige; infamy; credibility
- **ideological**: belief systems; political doctrines; moral frameworks; ideological conflicts
- **ethical**: moral norms; ethical dilemmas; accepted behavior; contested ethics

### 12. Religious, theological and divine domains

- **religious**: faiths; worship; clergy; temples; rituals; doctrine; religious communities
- **theological**: doctrine; cosmology; divine nature; heresies; theological disputes
- **ecclesiastical**: church hierarchy; clergy; dioceses; temple administration; ecclesiastical offices
- **divine**: deities; divine intervention; miracles; chosen agents; divine artifacts
- **sacred**: holy places; relics; consecrated objects; pilgrimage; sacred geography
- **ritual**: rites; sacrifices; prayers; ceremonial procedures; initiations
- **clerical**: priests; orders; clerical magic; responsibilities; ranks
- **monastic**: monasteries; orders; vows; discipline; property; education
- **heretical**: heresies; schisms; suppressed doctrine; religious dissent
- **cultic**: cults; secret worship; initiations; leaders; cells; rituals
- **prophetic**: prophecies; prophets; visions; interpretations; fulfillment conditions
- **eschatological**: end-times beliefs; apocalypse; final battles; salvation; cosmic cycles
- **soteriological**: salvation; damnation; redemption; afterlife conditions
- **angelological**: celestials; angels; divine servants; hierarchies; missions
- **demonological**: demons; fiends; cults; summoning; infernal hierarchies

### 13. Arcane, magical and occult domains

- **arcane**: magic; mages; spells; magical institutions; artifacts; magical infrastructure
- **magical**: sources of magic; techniques; costs; limitations; users; applications
- **thaumaturgical**: practical magic; spellcraft; magical engineering; ritual techniques; magical mechanisms
- **sorcerous**: innate magic; bloodlines; wild magic; sorcerous traditions
- **wizardly**: wizard schools; spellbooks; academies; research; apprenticeships
- **ritualistic**: ritual magic; components; timing; participants; consequences
- **enchantment**: enchanted objects; enchantment methods; permanence; costs; effects
- **alchemical**: alchemy; reagents; laboratories; potions; transformations; recipes
- **necromantic**: undeath; necromancy; corpses; souls; forbidden practices
- **conjuration**: summoning; binding; teleportation; planar calling
- **divinatory**: scrying; prophecy; foresight; omens; information magic
- **illusionistic**: illusions; deception; concealment; perceptual manipulation
- **transmutational**: transformation; polymorph; material alteration; magical manufacturing
- **abjurative**: wards; protections; seals; countermagic; magical security
- **evocational**: destructive magic; elemental magic; battle magic
- **magical-economic**: spell services; magical commodities; enchanted goods; magical labor markets
- **magical-industrial**: magical manufacturing; enchanted infrastructure; large-scale spell use
- **magical-legal**: licensed magic; prohibited magic; magical crimes; enforcement
- **magical-ecological**: magical pollution; ley lines; magical species; altered ecosystems
- **magical-geographical**: mythals; dead-magic zones; wild-magic zones; ley lines; magical boundaries
- **occult**: hidden lore; forbidden rites; secret societies; taboo knowledge
- **esoteric**: obscure knowledge; coded traditions; lost teachings; hidden correspondences
- **hermetic**: secret magical philosophies; symbolic systems; initiatory knowledge
- **runological**: runes; magical writing; sigils; inscriptions; runic systems
- **onomastic**: true names; naming magic; name traditions; magical nomenclature
- **astrological**: stars; constellations; omens; celestial influence; magical astrology

### 14. Cosmological and metaphysical domains

- **cosmological**: planes; cosmic structure; divine realms; planar relations; cosmic cycles
- **metaphysical**: souls; reality; causality; magic; identity; metaphysical laws
- **ontological**: what kinds of beings exist; categories of existence; transformations between categories
- **planar**: planes; portals; planar routes; planar inhabitants; planar hazards
- **astral**: Astral Plane; astral travel; astral entities; astral geography
- **ethereal**: Ethereal Plane; phase states; ethereal creatures; crossings
- **elemental**: elemental planes; elemental forces; elemental creatures; resources
- **afterlife**: death; souls; judgment; afterlife destinations; resurrection
- **soul**: souls; soul ownership; soul damage; soul transfer; resurrection implications
- **fate**: destiny; prophecy; fate manipulation; predestination; cosmic patterns
- **temporal**: time; time travel; temporal anomalies; chronology; temporal effects
- **dimensional**: dimensions; pocket realms; extradimensional spaces; dimensional boundaries

### 15. Geographic and spatial domains

- **geographical**: regions; terrain; borders; settlements; spatial relationships; climate
- **topographical**: elevation; slopes; valleys; peaks; surface form; terrain difficulty
- **cartographic**: maps; coordinates; scale; routes; map discrepancies; unexplored regions
- **territorial**: controlled territory; claims; frontiers; contested zones
- **regional**: regions; subregions; regional identities; regional systems
- **locational**: coordinates; relative positions; distance; adjacency
- **route**: roads; sea lanes; trails; rivers; passes; shortcuts
- **distance**: distance; travel time; movement speed; route cost
- **borderland**: frontiers; marches; liminal regions; contested settlements; mixed cultures

### 16. Geological, hydrological and climatological domains

- **geological**: rock; mineral deposits; tectonics; caves; volcanic activity; terrain formation
- **geomorphological**: landforms; erosion; deposition; coastal formation; river valleys
- **mineralogical**: minerals; ores; gemstones; deposits; mining value
- **hydrological**: rivers; lakes; aquifers; drainage; water supply; flooding
- **oceanographic**: currents; tides; depths; seas; ocean conditions
- **coastal**: coastlines; beaches; cliffs; estuaries; coastal hazards
- **fluvial**: rivers; tributaries; crossings; river trade; flooding
- **limnological**: lakes; lake ecosystems; lake transport; water chemistry
- **climatological**: climate; rainfall; temperatures; seasonality; climate zones
- **meteorological**: weather; storms; winds; fog; precipitation; extreme events
- **seasonal**: seasonality; migrations; harvests; weather cycles; seasonal commerce
- **disaster**: earthquakes; floods; storms; fires; magical disasters; recovery

### 17. Biological and ecological domains

- **ecological**: ecosystems; species interactions; habitats; environmental pressures
- **biological**: organisms; reproduction; physiology; adaptation; biological systems
- **zoological**: animals; monsters; behavior; diet; reproduction; range
- **botanical**: plants; crops; herbs; distribution; uses; seasonality
- **mycological**: fungi; spores; fungal ecosystems; culinary; medicinal; magical uses
- **entomological**: insects; swarms; pollination; disease vectors; agricultural effects
- **marine-biological**: marine species; fisheries; reefs; marine ecosystems
- **forestry**: forests; timber; woodland ecology; forest management; logging
- **biodiversity**: species richness; rare species; ecological hotspots; extinctions
- **conservation**: protected areas; sacred groves; resource restrictions; stewardship
- **invasive-species**: introduced species; ecological disruption; spread; control
- **predation**: predators; prey; hunting patterns; population effects
- **food-web**: producers; consumers; predators; scavengers; trophic relationships

### 18. Wilderness and survival domains

- **wilderness**: wild terrain; hazards; routes; resources; campsites; predators
- **survival**: water; food; shelter; navigation; temperature; disease; exposure
- **exploration**: unknown regions; expeditions; maps; discoveries; exploration risks
- **navigation**: landmarks; stars; currents; compasses; magical navigation
- **frontier**: new settlements; wilderness pressure; border conflicts; resource claims
- **hunting**: game animals; hunting methods; seasons; hunting rights
- **foraging**: edible plants; medicinal plants; seasonality; dangerous lookalikes

### 19. Urban and settlement domains

- **urban**: districts; streets; housing; markets; utilities; policing; urban social structure
- **urbanistic**: city planning; zoning; density; street networks; expansion
- **settlement**: settlements; population; economy; government; defenses; services
- **architectural**: buildings; styles; materials; construction methods; functions
- **residential**: housing; neighborhoods; occupancy; tenure; class distribution
- **civic**: public buildings; squares; monuments; civic institutions; municipal identity
- **infrastructural**: roads; bridges; sewers; ports; water; communications; utilities
- **sanitation**: waste; sewage; water cleanliness; latrines; garbage; disease prevention
- **housing**: building types; rents; overcrowding; ownership; housing quality
- **district**: districts; functions; demographics; landmarks; governance; reputation
- **neighborhood**: local identity; businesses; gangs; social networks; everyday life
- **street-level**: shops; stalls; traffic; signage; street vendors; patrols; crowds

### 20. Maritime domains

- **maritime**: ships; ports; sailors; shipping; routes; cargo; maritime culture
- **nautical**: navigation; seamanship; rigging; ship handling; weather; tides
- **shipping**: cargo; schedules; shipping firms; freight rates; routes; risks
- **port**: harbors; docks; warehouses; customs; shipyards; labor
- **shipbuilding**: shipyards; timber; craftsmen; ship types; construction; repair
- **seafaring**: sailors; shipboard life; customs; discipline; recruitment
- **piratical**: piracy; raiding; pirate bases; fences; naval responses
- **fishing**: fisheries; fleets; species; seasons; processing; markets
- **naval-logistical**: bases; victualling; repair; crew replacement; supply routes

### 21. Technological and scientific domains

- **technological**: technologies; tools; machines; processes; innovations; limitations
- **mechanical**: machines; gears; engines; mechanisms; maintenance
- **engineering**: construction; design; materials; infrastructure; technical constraints
- **civil-engineering**: roads; bridges; canals; dams; walls; drainage; public works
- **military-engineering**: fortifications; siege works; bridges; demolition; field works
- **hydraulic-engineering**: aqueducts; canals; pumps; mills; drainage
- **metallurgical**: metals; smelting; forging; alloys; material properties
- **material-science**: wood; stone; metal; glass; ceramics; magical materials
- **scientific**: natural philosophy; experimentation; theories; discoveries; instruments
- **astronomical**: stars; planets; calendars; navigation; celestial events
- **mathematical**: measurement; accounting; geometry; statistics; calculation systems
- **medical**: medicine; healers; disease; surgery; treatments; hospitals
- **pharmaceutical**: medicines; herbs; potions; dosage; manufacture; trade
- **epidemiological**: disease spread; outbreaks; mortality; vectors; containment
- **anatomical**: body structures; species anatomy; injury; physiology
- **technical-knowledge**: specialists; manuals; training; trade secrets; skill transmission

### 22. Information, knowledge and communication domains

- **information**: messages; records; rumors; news; intelligence; information flows
- **communication**: messengers; letters; signals; magical communication; speed; reach
- **postal**: couriers; routes; post stations; costs; reliability
- **scribal**: scribes; copying; records; administrative texts; literacy
- **archival**: archives; records; preservation; access; classification; lost records
- **library**: libraries; collections; librarians; access; rare texts
- **educational**: schools; academies; apprenticeships; curricula; teachers; access
- **academic**: universities; scholars; disciplines; research; patronage
- **epistemological**: how knowledge is produced; what counts as evidence; authority; uncertainty
- **knowledge**: known facts; secrets; expertise; restricted knowledge; knowledge distribution
- **literacy**: reading; writing; numeracy; class differences; institutional literacy
- **propaganda**: official narratives; persuasion; censorship; messaging; mythmaking
- **rumor**: rumors; origins; spread; credibility; social effects
- **censorship**: banned texts; restricted speech; information control; enforcement
- **recordkeeping**: registries; tax records; legal records; church records; commercial ledgers

### 23. Historical domains

- **historical**: events; chronology; causes; participants; consequences
- **chronological**: dates; eras; sequences; before-after relationships
- **genealogical**: lineages; families; descent; succession; marriages
- **dynastic**: dynasties; rulers; successions; marriages; claims
- **military-historical**: wars; battles; campaigns; military reforms; long-term effects
- **economic-historical**: trade changes; crises; growth; decline; industrial shifts
- **institutional-historical**: founding; reforms; mergers; decline; institutional continuity
- **archaeological**: ruins; artifacts; layers; material evidence; ancient settlements
- **historiographical**: competing accounts; historians; bias; disputed interpretation
- **memory**: collective memory; monuments; trauma; commemorations; myths
- **legacy**: long-term consequences; surviving institutions; cultural residue; unresolved claims

### 24. Mundane everyday-life domains

- **mundane**: daily routines; household life; food; work; chores; leisure
- **domestic**: households; cooking; cleaning; childcare; furniture; domestic labor
- **occupational**: jobs; workplaces; tools; schedules; status; pay
- **professional**: professions; qualifications; training; institutions; norms
- **service**: inns; laundries; transport; healers; entertainment; repairs
- **leisure**: games; sports; taverns; festivals; hobbies
- **recreational**: sports; gambling; hunting; social clubs; entertainment
- **hospitality**: inns; taverns; guest customs; lodging; meals; pricing
- **retail**: shops; stalls; merchants; goods; opening patterns; customers
- **household-economy**: household income; expenses; home production; servants; dependents

### 25. Adventure and gameable-content domains

- **adventure**: hooks; conflicts; threats; mysteries; rewards; locations; NPC motivations
- **hook**: problems; rumors; opportunities; requests; discoveries
- **mystery**: questions; clues; suspects; secrets; false leads; revelations
- **threat**: threats; targets; severity; timelines; vulnerabilities
- **quest**: objective; patron; opposition; reward; complications; consequences
- **dungeon**: rooms; hazards; factions; treasure; routes; secrets
- **encounter**: participants; objectives; terrain; hazards; complications
- **NPC-motivation**: goals; fears; needs; relationships; leverage; secrets
- **reward**: treasure; status; information; access; favors; magical items
- **clue**: evidence; location; meaning; reliability; connections
- **secret**: hidden truths; who knows; who wants it hidden; consequences
- **rumor-hook**: rumors; truth level; source; adventure implications
- **conflict**: actors; interests; stakes; pressures; escalation; possible resolutions
- **dilemma**: competing values; tradeoffs; beneficiaries; victims; consequences
- **timer**: deadlines; escalation clocks; seasonal windows; countdowns
- **failure-state**: what happens if players do nothing; partial failure; cascading consequences
- **opportunity**: trade opportunities; political opportunities; exploration; treasure; alliances; exploitation

### 76. Cross-domain geographic and synthetic domains

- **geoeconomic**: geography of trade; market access; resource geography; economic corridors; sanctions; chokepoints; regional production; capital flows
- **geostrategic**: strategic geography; chokepoints; buffer zones; force projection; resource security; routes; frontiers
- **geocultural**: culture across space; regional identity; cultural zones; diffusion; border cultures; cultural landscapes
- **geolinguistic**: languages across space; dialect regions; linguistic borders; trade languages; language diffusion
- **georeligious**: religion across space; pilgrimage geography; holy regions; religious frontiers; missionary diffusion
- **geodemographic**: population geography; density; migration corridors; settlement distribution; demographic frontiers
- **ethnolinguistic**: language communities; ethnic-linguistic identity; multilingual regions; language shift; diaspora speech
- **biogeographical**: species distribution; ecoregions; migration ranges; biological barriers; habitat geography
- **geophysical**: physical earth processes; terrain formation; tectonics; gravity; seismicity; geophysical hazards
- **geochemical**: mineral chemistry; soil chemistry; water chemistry; resource signatures; contamination
- **geotechnical**: ground conditions; foundations; slope stability; excavation; tunneling; construction constraints

### 77. Material, environmental and mobility domains

- **nature**: natural systems; flora; fauna; landscape; seasons; natural cycles; human-nature interaction
- **environmental**: pollution; deforestation; erosion; flooding; drought; habitat loss; resource depletion; environmental change
- **resource**: raw materials; food sources; mines; forests; fisheries; farmland; magical resources; ownership; scarcity
- **transport**: vehicles; mounts; ships; roads; canals; freight; passenger transport; cost; speed; capacity
- **travel**: routes; travel time; waypoints; tolls; border crossings; transport methods; seasonality; navigation
- **energy**: fuel; firewood; coal; water power; wind power; magical power; energy production; distribution; scarcity
- **land-use**: farmland; pasture; forest; urban land; estates; commons; mines; sacred land; military land; land disputes
- **food-system**: food production; ingredients; preservation; markets; imports; exports; scarcity; storage; food supply chains
- **health**: medicine; healers; hospitals; disease; sanitation; childbirth; injury; mortality; public health
- **hazard**: natural hazards; magical hazards; military hazards; disease; crime; monsters; severity; warning signs; mitigation
- **material-culture**: tools; furniture; weapons; clothing; utensils; craftsmanship; materials; status markers; regional styles
- **monster-ecology**: creatures; habitats; territories; diet; behavior; migration; predators; prey; settlement effects; economic effects
- **infrastructure-systems**: roads; bridges; ports; canals; sewers; water supply; warehouses; communications; capacity; maintenance
- **water-systems**: water sources; aqueducts; wells; cisterns; irrigation; drainage; distribution; water security
- **waste-systems**: sewage; garbage; industrial waste; magical waste; collection; disposal; reuse; pollution

### 78. Cognitive, philosophical and symbolic domains

- **cognitive**: perception; memory; reasoning; attention; decision-making; belief formation; cognitive bias
- **philosophical**: philosophies; schools of thought; ethics; metaphysics; epistemology; political philosophy; natural philosophy
- **symbolic**: symbols; ritual meanings; colors; emblems; metaphors; status signs; coded meanings
- **sociolinguistic**: language and status; register; code-switching; prestige dialects; occupational language; social language variation
- **folkloric**: folklore; legends; folk beliefs; oral tradition; superstitions; local tales
- **mythological**: myths; cosmogonies; hero cycles; founding stories; divine narratives; mythic archetypes
- **iconographic**: visual symbols; religious imagery; political imagery; emblems; motifs; representation
- **rhetorical**: persuasion; oratory; argument; political rhetoric; religious rhetoric; propaganda techniques
- **narrative**: stories; narrative frames; plot traditions; collective narratives; identity stories; historical narratives
- **hermeneutical**: interpretation; textual meaning; scriptural interpretation; legal interpretation; symbolic reading; competing readings

### 79. Scientific and historical specialty domains

- **pathological**: disease processes; injury processes; symptoms; pathology; causes of illness; mortality
- **pharmacological**: drug effects; dose; toxicity; interactions; medicinal compounds; pharmacodynamics
- **toxicological**: poisons; toxins; exposure; dose; symptoms; antidotes; contamination
- **paleontological**: fossils; extinct species; ancient ecosystems; deep biological history; fossil evidence
- **paleoclimatological**: past climate; climate proxies; historical climate shifts; ancient droughts; glaciation
- **archaeozoological**: animal remains; diet; domestication; hunting; past animal economies; faunal evidence
- **archaeobotanical**: plant remains; ancient crops; diet; agriculture; wood use; botanical evidence
- **numismatic**: coins; mints; coin circulation; iconography; debasement; dating; monetary evidence
- **paleographic**: historical handwriting; scripts; dating texts; scribal traditions; manuscript hands
- **codicological**: manuscripts as objects; bindings; quires; materials; book production; provenance
- **sigillographic**: seals; signets; authority marks; authentication; institutional identity
- **epigraphic**: inscriptions; monuments; dating; public texts; dedications; lapidary writing

### 80. Systems and comparative analytical domains

- **systemic**: systems; components; interactions; feedback; emergent behavior; boundaries; dependencies
- **structural**: structure; hierarchy; institutional arrangement; network position; constraints; roles
- **functional**: function; role; purpose; system contribution; failure modes; substitution
- **comparative**: comparison; similarities; differences; peer regions; institutional comparison; cross-era comparison
- **network-analytic**: network centrality; hubs; bridges; clusters; isolation; redundancy; connectivity
- **causal-comparative**: comparative causation; different outcomes; shared causes; necessary conditions; sufficient conditions
- **institutional-comparative**: institution comparison; governance comparison; capacity comparison; institutional performance; institutional variation
- **spatial-analytic**: spatial distribution; distance effects; clusters; corridors; hinterlands; spatial dependency
- **temporal-analytic**: change over time; lags; cycles; path dependency; turning points; temporal comparison
- **distributional**: who gains; who loses; distribution of costs; distribution of benefits; inequality effects; incidence
- **complexity**: complex adaptive systems; emergence; nonlinearity; interdependence; tipping points; uncertainty
- **diffusion**: spread of ideas; technology; religion; culture; disease; institutions; routes of diffusion

## System layer

### 28. Causal relationship layers

- **causal**: cause; effect; contributing factor; necessary condition; sufficient condition; trigger; amplifier; inhibitor; feedback; consequence; unintended consequence

### 29. Dependency layer

- **dependency**: critical dependencies; weak dependencies; substitutable dependencies; non-substitutable dependencies; single points of failure; external dependencies

### 30. Flow layers

- **flow**: what moves; from where; to where; through whom; through what route; at what rate; at what cost; with what bottlenecks

### 31. Pressure layer

- **pressure**: economic pressure political pressure demographic pressure military pressure environmental pressure social pressure religious pressure technological pressure resource pressure

### 32. Incentive layer

- **incentive**: actor; goal; reward; cost; constraint; risk; alternative; likely behavior

### 33. Power layer

- **power**: formal authority informal influence economic power military power religious power magical power informational power social prestige institutional power coercive power

### 34. Capability layer

- **capability**: what an actor can actually do; resources; skills; capacity; reach; constraints

### 35. Capacity layer

- **capacity**: maximum throughput; normal throughput; spare capacity; overloaded capacity; growth capacity

### 36. Constraint layer

- **constraint**: geographic constraints resource constraints legal constraints political constraints social constraints technological constraints magical constraints financial constraints labor constraints logistical constraints seasonal constraints

### 37. Vulnerability layer

- **vulnerability**: single points of failure; exposed resources; unprotected routes; political weaknesses; economic weaknesses; magical weaknesses

### 38. Resilience layer

- **resilience**: redundancy; reserves; substitution; alliances; emergency capacity; institutional flexibility

### 39. Bottleneck and chokepoint layer

- **bottleneck**: capacity bottlenecks transport bottlenecks bureaucratic bottlenecks resource bottlenecks knowledge bottlenecks political bottlenecks
- **chokepoint**: mountain passes bridges ports straits roads city gates canals trade hubs magical portals

### 40. Substitution layer

- **substitution**: resource substitutes trade-route substitutes labor substitutes technological substitutes magical substitutes political substitutes

### 41. Competition layer

- **competition**: actors competing for resources markets territory labor prestige political influence trade routes divine followers magical resources

### 42. Conflict layer

- **conflict**: actors; causes; stakes; resources; escalation; constraints; possible resolution; current state

### 43. Cooperation layer

- **cooperation**: shared interests; joint institutions; alliances; interdependence; collective action

### 44. Feedback-loop layer

- **feedback**: positive feedback loops negative feedback loops stabilizing loops destabilizing loops

### 45. Threshold layer

- **threshold**: points where gradual pressure causes sudden change

### 46. Cascade layer

- **cascade**: first-order effect second-order effect third-order effect systemic consequences

### 47. Counterfactual layer

- **counterfactual**: if X changed, what would probably follow?

### 48. Opportunity layer

- **opportunity**: economic opportunities political opportunities military opportunities criminal opportunities adventure opportunities technological opportunities magical opportunities

### 49. Risk layer

- **risk**: hazard; probability; exposure; impact; mitigation; warning indicators

### 50. Provenance layer

- **provenance**: source book page section edition author quote context certainty

### 51. Epistemic layer

- **epistemic**: explicit fact strong implication weak implication inference speculation contradiction unknown

### 52. Contradiction layer

- **contradiction**: fact conflicts date conflicts map conflicts population conflicts identity conflicts edition conflicts source conflicts

### 54. Change layer

- **change**: growth decline centralization fragmentation urbanization migration industrialization militarization commercialization secularization magical expansion environmental degradation

### 55. Trend layer

- **trend**: increasing; decreasing; stable; cyclical; volatile; uncertain

### 53. Temporal-state layer

- **temporal state**: state; valid_from; valid_until; era; historical state

### 56. Network layer

- **network**: trade network; political network; kinship network; religious network; criminal network; shipping network; road network; information network; alliance network; portal network; financial network

### 81. Cross-domain coupling layer

- **cross-domain coupling**: economy-politics; economy-military; demography-labor; ecology-economy; geography-logistics; infrastructure-trade; magic-technology; religion-politics; crime-governance; information-power; disease-trade; climate-agriculture

### 82. Shock-propagation layer

- **shock propagation**: shock source; transmission channel; first-order effect; second-order effect; amplification; damping; affected systems

### 83. Lag and delay layer

- **lag and delay**: time lag; implementation delay; travel delay; information delay; production delay; response delay; delayed consequence

### 84. Adaptation layer

- **adaptation**: actor adaptation; institutional adaptation; market response; ecological adaptation; technological adaptation; behavioral response

### 85. Path-dependency layer

- **path dependency**: historical lock-in; increasing returns; institutional inertia; legacy infrastructure; irreversibility; switching cost

### 86. Externality layer

- **externality**: positive externality; negative externality; spillover; unpriced cost; unpriced benefit; third-party effect

### 87. Trade-off layer

- **trade-off**: competing objective; opportunity cost; benefit; cost; constraint; distributional consequence

### 88. Distributional-effect layer

- **distributional effect**: winners; losers; incidence; class effect; regional effect; faction effect; inequality

### 89. Institutional-friction layer

- **institutional friction**: bureaucratic delay; jurisdiction conflict; coordination cost; procedural bottleneck; organizational inertia; implementation gap

### 90. Equilibrium and disequilibrium layer

- **equilibrium and disequilibrium**: stable state; unstable state; market clearing; persistent imbalance; adjustment process; disequilibrium

### 91. Volatility layer

- **volatility**: variance; instability; price swings; political volatility; supply volatility; shock sensitivity

### 92. Leverage-point layer

- **leverage point**: high-impact intervention; control point; chokepoint; policy lever; critical actor; small-change large-effect

## Inference layer

### 65. Missing-information layer

- **missing**: important information that should exist but is absent

### 66. Plausibility layer

- **plausibility**: economic plausibility geographic plausibility demographic plausibility military plausibility technological plausibility ecological plausibility institutional plausibility

### 68. Identity-resolution layer

- **identity**: same entity? different entities? alias? title? incarnation? historical version?

### 72. Perspective layer

- **perspective**: author perspective faction perspective regional perspective religious perspective political bias cultural bias unreliable narration

### 57. Spatial-inference layer

- **spatial inference**: relative position; trade paths; watersheds; hinterlands; natural frontiers; military routes

### 58. Economic-inference layer

- **economic inference**: resources; population; transport; technology; institutions; industries; imports; exports; shortages; trade partners

### 59. Demographic-inference layer

- **demographic inference**: population; birth rate; death rate; migration; war; disease; food supply; labor; settlement expansion; military manpower

### 60. Political-inference layer

- **political inference**: institutions; power distribution; legitimacy; factions; pressures; stability; coup risk; rebellion risk; succession; policy

### 61. Military-inference layer

- **military inference**: population; wealth; technology; terrain; logistics; army potential; mobilization; defense; campaign reach; naval capacity

### 62. Ecological-inference layer

- **ecological inference**: climate; terrain; flora; fauna; settlement; resource extraction; ecosystem pressure; agriculture; degradation

### 63. Urban-inference layer

- **urban inference**: population; trade; government; geography; infrastructure; districts; land values; class geography; markets; crime; traffic

### 64. Adventure-inference layer

- **adventure inference**: political tensions; economic dependencies; criminal networks; historical grievances; mysteries; ecological hazards; adventure opportunities

### 67. Normalization layer

- **normalization**: canonical entity; preferred name; aliases; spellings; historical names; translations

### 69. Granularity layer

- **granularity**: hierarchy; partonomy; settlement hierarchy; economic hierarchy

### 70. Scale layer

- **scale**: individual; household; neighborhood; settlement; regional; national; continental; global; planar; cosmic

### 71. Certainty layer

- **certainty**: confidence; explicit; inferred; estimated; speculative; source quality; evidence count

### 73. Contradictory-perspective layer

- **contradictory perspective**: viewpoint; faction perspective; regional perspective; competing narratives

### 74. Salience layer

- **salience**: background; minor; important; major; defining; world-changing

### 75. Simulation-readiness layer

- **simulation readiness**: descriptive; relational; quantifiable; time-sensitive; causal; simulatable

### 100. Geoeconomic-inference layer

- **geoeconomic inference**: trade power; resource leverage; sanctions; economic coercion; strategic dependencies; commercial corridors

### 101. Trade-network-inference layer

- **trade network inference**: origins; destinations; commodities; intermediaries; routes; chokepoints; competing routes; hub importance

### 102. Supply-chain-inference layer

- **supply chain inference**: inputs; processing; storage; transport; distribution; single points of failure; substitutes

### 103. Fiscal-inference layer

- **fiscal inference**: tax base; revenue capacity; expenditure pressure; public debt; fiscal stress; tax incidence

### 104. Institutional-inference layer

- **institutional inference**: capacity; legitimacy; coordination; implementation; capture; inertia; institutional failure

### 105. Legal-inference layer

- **legal inference**: jurisdiction; enforcement; legal conflict; rights; compliance incentives; regulatory effects

### 106. Diplomatic-inference layer

- **diplomatic inference**: bargaining position; alliance reliability; deterrence; recognition; treaty incentives; escalation

### 107. Logistics-inference layer

- **logistics inference**: throughput; lead time; route capacity; storage; resupply; bottlenecks; alternate routes

### 108. Infrastructure-inference layer

- **infrastructure inference**: capacity; maintenance; coverage; failure points; service area; network effects; investment need

### 109. Technological-diffusion-inference layer

- **technological diffusion inference**: innovation source; adoption; diffusion routes; barriers; complements; substitution; lock-in

### 110. Knowledge-diffusion-inference layer

- **knowledge diffusion inference**: information source; transmission; gatekeepers; literacy; institutions; censorship; knowledge gaps

### 111. Magical-economy-inference layer

- **magical economy inference**: magical labor; spell services; enchanted goods; reagents; magical infrastructure; substitution with mundane technology

### 112. Religious-influence-inference layer

- **religious influence inference**: clerical authority; temple networks; doctrine; pilgrimage; legitimacy; charity; religious conflict

### 113. Cultural-diffusion-inference layer

- **cultural diffusion inference**: custom spread; language spread; fashion spread; foodways; ritual diffusion; trade-mediated culture

### 114. Migration-inference layer

- **migration inference**: push factors; pull factors; routes; diaspora; labor effects; settlement effects; political effects

### 115. Disease-inference layer

- **disease inference**: transmission; vectors; trade routes; crowding; mortality; containment; second-order economic effects

### 116. Environmental-inference layer

- **environmental inference**: resource pressure; pollution; habitat loss; flooding; drought; feedback with economy and settlement

### 117. Resource-depletion-inference layer

- **resource depletion inference**: stock; extraction rate; renewal; scarcity; price effects; substitution; conflict

### 118. Maritime-inference layer

- **maritime inference**: port hierarchy; shipping lanes; seasonality; naval reach; freight cost; piracy risk; maritime chokepoints

### 119. Security-inference layer

- **security inference**: threat surface; response capacity; surveillance; border control; internal security; critical vulnerabilities

### 120. Criminal-network-inference layer

- **criminal network inference**: cells; brokers; safehouses; territories; contraband flows; corrupt protection; network resilience

### 121. Succession-inference layer

- **succession inference**: claims; heirs; legitimacy; elite support; military backing; foreign intervention; civil conflict risk

### 122. Cross-domain-consequence-inference layer

- **cross-domain consequence inference**: first-order effect; second-order effect; third-order effect; cross-domain spillover; feedback; uncertainty

