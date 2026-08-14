# Design Tokens

Concrete values implementing `design/README.md`'s principles, for `app/`'s SwiftUI implementation to consume directly.

## Material

- **Surface:** `.ultraThinMaterial` (SwiftUI system material) as the default surface — real glassmorphism via the system compositor, not a hand-rolled blur+opacity hack.
- **Blur radius:** system-default for `.ultraThinMaterial`; do not override unless a specific screen proves illegible against busy camera-preview content behind it (the boundary-setting screen is the one place this might be needed).

## Corner radius

- **Controls (buttons, cards):** 16pt — matches iOS system continuous-corner convention, avoids a custom look that fights the platform.
- **Sheets/modals:** 24pt (top corners only), matching iOS sheet presentation defaults.

## Color

- **Accent:** single accent color reserved for active/interactive state (call connecting, boundary-edit-mode handles). Not yet chosen — pick once the TAYF wordmark/identity exists, if it does; otherwise default to system accent (`Color.accentColor`) rather than inventing a brand color under time pressure.
- **Everything else:** system semantic colors (`Color.primary`, `Color.secondary`, system backgrounds) — no custom palette. This is a restraint choice, not a placeholder: a custom palette is brand work the hackathon timeline doesn't support (`design/README.md` non-goals).

## Type

- **System font (SF Pro via `.font(.system(...))`), Dynamic Type-respecting sizes only.** No custom typeface — same reasoning as color.
- **Hierarchy via weight:** `.semibold`/`.bold` for primary actions and state (call status), `.regular` for secondary/supporting text. No more than two weights on screen at once.

## Motion

- **Standard SwiftUI implicit animations** (`.easeInOut`, system defaults) for state transitions. No custom easing curves or durations — per `design/README.md` rule 4, motion here is confirmation, not a design opportunity.
