# The Forensic Semantic Lexicon

This directory is reserved for the JSON configuration files containing the multi-prompt textual anchors.

### Purpose
Instead of basic class names like "weapon", the lexicon defines arrays of dense descriptions (e.g., "a forensic photograph of a seized metallic revolver"). The vectors of these descriptions are averaged to form the robust Semantic Centroids used in the main engine.

### Lexicon Anchors

| Category | Textual Prompts (Anchors) |
|---|---|
| **Weapons** (Armas) | • *a physical metallic handgun or pistol on a surface*<br>• *a real revolver seized by police in a forensic scene* |
| **Drugs** (Drogas) | • *a cigarette or hand-rolled joint in someone's hand*<br>• *closed packs of cigarettes on a table*<br>• *bags with tobacco or rolling paper*<br>• *marijuana leaves or dried cannabis buds*<br>• *suspicious white powder in small plastic bags* |
| **Currency** (Dinheiro) | • *bundles of paper bank notes spread on a table*<br>• *thick stacks of physical currency seized by police* |
| **Others** (Outros) | • *industrial paint cans with labels*<br>• *metallic buckets of paint*<br>• *a frog inside a muddy hole in the ground*<br>• *red strawberry-shaped gummy candy or sweet*<br>• *a food tray or lunch box with a plastic soda bottle*<br>• *electric hair clipper or hair trimming machine*<br>• *people riding motorcycles in the mud*<br>• *shaving or trimming animal hair with a machine*<br>• *a person using a hair clipper on someone*<br>• *a smartphone or mobile phone*<br>• *a person speaking into a microphone*<br>• *everyday household objects and non-forensic items* |

### Files
- `custom_prompts.json`: The raw text arrays for each forensic category, defining the expert descriptions (fully listed above).
- `centroids_final.pkl`: Pre-computed normalized vectors for fast evaluation and deployment.
