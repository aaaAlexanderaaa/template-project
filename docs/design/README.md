# Frontend surface contracts

Each user-visible surface gets one living contract. Use
`templates/frontend-surface.md`.

The required pair is:

- **Raw layer:** dated stakeholder language, observations, rejected attempts,
  and changed requirements in the source's own words.
- **Translated layer:** engineering states, transitions, layout, size,
  interaction, accessibility, responsive behavior, and evidence expectations.

Every `###` subsection inside the translated layer contains at least one
`- from: raw[N]` line; place additional citations next to a more specific claim
when one subsection translates multiple sources. The checker requires at least
one dated raw anchor and one translated subsection, resolves every translated
citation, rejects uncited subsections, and requires every raw anchor to be
cited. Citations elsewhere in the document do not count. When feedback says
the result is wrong, classify whether the source was ambiguous, the translation
was wrong, the requirement changed, or implementation regressed.

If the surface maintains known abnormality classes, use the structured
`abnormality[slug]` records in the template. The section is optional; once
present, its evidence and verification references are checked.
