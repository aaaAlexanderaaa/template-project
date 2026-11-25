---
doc_type: contract
status: current
authority: normative
---

# Information Organization Discipline

This contract covers how to organize information for readers: project
documents (`README.md`, `ARCHITECTURE.md`, specs, ADRs, guides), the
information architecture of user interfaces (what goes on which screen, in
which order, under which name), and reader-facing knowledge content (courses,
knowledge maps, reference libraries, reports). The rules below come from
established practice in information architecture (Rosenfeld, Morville & Arango,
*Information Architecture*; Richard Saul Wurman's LATCH schemes), technical
documentation (the Diátaxis framework), business writing (Barbara Minto's
pyramid principle), and information foraging research (Pirolli & Card's
"information scent").

Where each fact is stored is a separate question owned by the documentation
map (`docs/README.md`): one fact has one authoritative file. This contract decides how that information is
grouped, ordered, layered, named, and presented to the person reading it.

<!-- required-reading: reader-task-first -->
## 1. Start From the Reader and the Task

1. **Name the reader and the job before arranging anything**: Write down who
   reads this, what question they arrive with or what decision they must make,
   and what they already know. A design document for an owner who is not a
   software architect, an API reference for a developer in the middle of
   coding, and a knowledge map for a learner each need a different order.
2. **Organize by the reader's task, not by how the producer is organized**:
   Code folder layout, team structure, build order, or the order in which the
   author learned the topic are poor default structures for readers. Use them
   only when they match how the reader looks for things.
3. **Put the answer first**: Open each document, section, or screen with the
   conclusion, the current state, or the main action; follow with reasons, then
   detail and sources (pyramid principle / inverted pyramid). A reader who
   stops after the first paragraph should still leave with the most important
   point.
4. **Say what the reader can do next**: End task-oriented pages with the next
   step, the owning file, or the decision that is waiting, rather than a
   restatement.
<!-- /required-reading: reader-task-first -->

<!-- required-reading: organizing-schemes -->
## 2. Choose an Organizing Scheme and Keep Each Level Consistent

1. **Pick the scheme deliberately for each level**: The common schemes are by
   task, by audience, by topic or category, by time, by location, by hierarchy
   or importance, and alphabetical (Wurman's LATCH plus task and audience).
   State the chosen scheme in the parent's introduction when it is not obvious.
2. **One scheme per level**: Do not mix "by time" and "by topic" among siblings
   of the same parent. Use a second scheme one level down, or offer it as an
   alternative view (filter, index, timeline) of the same items.
3. **Siblings are comparable**: Items at the same level have similar size and
   depth, do not overlap in meaning, and together cover what the parent
   promises. Check for gaps and overlaps explicitly; treat "mutually exclusive,
   collectively exhaustive" as a review question rather than a reason to force
   artificial splits.
4. **Use the reader's words for labels**: Name sections, menu items, and nodes
   with the terms the reader would search for. A label should predict what is
   behind it ("information scent"); vague labels such as `Misc`, `Other`,
   `Utils`, `Overview 2` hide content. Keep one name per concept across docs,
   UI, and code.
5. **Keep positions and names stable**: Once readers learn where something is,
   renaming or reordering costs them. Change structure when it serves a clear
   reader need, and leave redirects or "moved to" notes for old links.
<!-- /required-reading: organizing-schemes -->

<!-- required-reading: layering-and-disclosure -->
## 3. Layer Detail and Keep Context Attached

1. **Three layers**: A summary layer (what this is and its current state), a
   working layer (what most readers need to act), and a detail or source layer
   (full data, raw records, proofs, history). Show the summary and working
   layers by default; open the detail layer on demand.
2. **Detail keeps its context**: Whenever a reader opens a detail, show where
   it sits (breadcrumb or parent summary), why it matters, and how to get back.
   Never present a detail that assumes the reader already knows its
   surroundings.
3. **Express relationships with the right structure**: Use hierarchy for
   "part of", sequence for steps and prerequisites, links or a network for
   cross-cutting relations, and a timeline for change over time. A single
   strict tree cannot express everything; add cross-links instead of copying
   content into several branches.
4. **Link instead of repeating**: When the same fact is needed in several
   places, keep it in one place and link to it with a one-line summary.
<!-- /required-reading: layering-and-disclosure -->

<!-- required-reading: form-follows-content -->
## 4. Choose the Form From the Question Being Answered

| Reader question | Best default form | Avoid |
|---|---|---|
| "How do these compare?" / "What is the value of X?" | Table (rows = items, columns = attributes) | Paragraphs that bury comparable values |
| "What do I do, in which order?" | Numbered steps | Unordered bullets for ordered work |
| "How are these parts connected or how does it flow?" | Diagram, when spatial layout explains faster than prose | Decorative diagrams that restate a list |
| "Why is it this way?" / "What causes what?" | Prose that states cause, mechanism, and limits | Fragmented bullets that drop the reasoning |
| "How did this change over time?" | Timeline or dated sequence | Undated narrative |
| "Where is X?" | Index, search, or alphabetical list | Deep navigation as the only path |

Mix forms inside one page when the reader has several questions, and keep each
block's form matched to its question.
<!-- /required-reading: form-follows-content -->

<!-- required-reading: document-types -->
## 5. Separate Documents by Reader Need

Project documents already carry an authority type (contract, spec, ADR, guide,
evidence) that decides which file wins in a conflict. Inside that system, also
keep each document or major section focused on one reader need (Diátaxis):

| Reader need | Document style | Example in this discipline |
|---|---|---|
| Learning by doing | Tutorial: a guided path with a working result | Onboarding walkthrough |
| Getting a specific task done | How-to: steps for one goal, assuming basic knowledge | `docs/guides/*.md` procedures |
| Looking something up | Reference: complete, consistent, scannable facts | Module specs, CLI flag tables, token lists |
| Understanding why | Explanation: background, trade-offs, alternatives | ADRs, design rationale |

Do not mix long rationale into reference tables or bury step-by-step
procedures inside explanations; link between them instead. Entry documents
(`AGENTS.md`, `README.md`, `docs/README.md`) act as maps: they tell the reader
what exists, where it lives, and which document answers which question.
<!-- /required-reading: document-types -->

<!-- required-reading: coverage-scope-freshness -->
## 6. Coverage, Scope, and Freshness of Knowledge Content

These rules apply whenever a project presents a body of knowledge to readers
(a course, a knowledge map, a reference library, a market or technology
overview), and to any document that describes the current state of a fast-
moving field.

1. **Scope by real-world impact, not by what the author knows**: Draw the
   field's full outline from external sources first (main applications,
   products and results, major awards and milestones, the industry chain, active
   research directions). Excluding a high-impact branch requires a stated reason
   tied to the reader's purpose; "the author is unfamiliar with it" or "the
   textbook does not cover it" are not reasons.
2. **Center the present when readers will apply it**: When readers learn a
   field to use it in current work, organize around the current landscape (main
   approaches, who does what, capabilities and limits, costs, direction of
   change). Principles explain why current practice works; history explains how
   the present formed.
3. **Breadth first at the top, depth one branch at a time**: Make the top layer
   complete (every major branch has an entry point) before taking any branch
   to deep detail. Mark top-layer and branch status separately.
4. **Sources must keep pace with the field**: Slow-changing material can rest
   on textbooks, standards, and systematic reviews. Fast-changing material
   (current products, models, prices, regulations, market structure) needs
   recent primary sources. The author's memory, including an AI model's
   training data, is not a source.
5. **Search to discover, not only to confirm**: Searching for names the author
   already knows only confirms memory. For current-state content, run date-
   anchored discovery searches ("releases since <date>", monthly trackers, the
   latest edition of annual reports) and extract candidates from the results.
   Record search terms and dates.
6. **Date every current-state fact**: Mark facts that will age with an as-of
   date and a review date, and show readers when content may be outdated. A
   coverage or "complete" claim is always stated as "complete as of <date>
   within <boundary>".
7. **Prove coverage claims**: Before calling a body of content complete, keep a
   coverage table that lists each item from the reference sources and from an
   impact list (major results, products, events) with its disposition:
   included, merged into another item, listed as a known gap, or excluded with a
   reason. Have the claim checked by an independent reviewer following
   [delivery-and-verification.md](delivery-and-verification.md#independent-review-definition),
   and let the owner confirm before the claim is published.
<!-- /required-reading: coverage-scope-freshness -->

<!-- required-reading: information-self-check -->
## 7. Self-Check Before Delivering Organized Information

1. Can a first-time reader say within 30 seconds what this is, what state it is
   in, and where to go next?
2. Is the organizing scheme of each level clear, with comparable siblings and
   no unexplained gaps or overlaps?
3. Do labels use the reader's words and predict their content?
4. Does every detail view show its context and a way back?
5. Does each block use the form that matches its question?
6. For knowledge content: are scope exclusions justified, current-state facts
   dated, and coverage claims backed by a coverage table and an independent
   check?
<!-- /required-reading: information-self-check -->
