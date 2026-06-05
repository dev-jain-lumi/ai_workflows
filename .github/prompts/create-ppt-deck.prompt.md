---
name: create-ppt-deck
description: "Create a presentation deck with repeatable inputs such as topic, audience, objective, and slide count. Uses the ppt-generation agent and writes outputs under Knowledge/presentations. Trigger phrases: create ppt deck, make slides, build presentation, create presentation, generate slide deck."
argument-hint: "Topic; audience; objective; slide count; output folder"
agent: "ppt-generation"
model: "GPT-5.4 (copilot)"
---
Create a presentation deck using these inputs:

- Topic: ${input:Topic or subject}
- Audience: ${input:Target audience}
- Objective: ${input:What the deck should achieve}
- Slide count: ${input:Number of slides or range}
- Output folder: ${input:Folder under Knowledge/presentations}

Instructions:
- Use the active ppt-generation agent behavior.
- Apply the design guidance from [.github/skills/ppt-design/SKILL.md](../skills/ppt-design/SKILL.md).
- Create source files under Knowledge/presentations only.
- Prefer Quarto `.qmd` when the user wants renderable slides; prefer single-file HTML only when explicitly requested.
- For repository decks, default the author to `Devashish Jain`.
- For repository decks, ensure the opening slide reads in this order: title, subtitle, author.
- Default to a Luminus corporate light theme unless the user explicitly asks for a darker theme.
- For Quarto outputs, create a top-level render entrypoint and keep all includes/assets in a working relative-path structure under the same presentation folder.
- Validate the deck by running `quarto render ... --to revealjs` before finishing whenever the user expects a live/renderable result.
- Before finishing a Quarto deck, verify the `.qmd` frontmatter includes `title`, `subtitle`, `author`, and `format.revealjs`, and verify the rendered HTML includes Reveal.js initialization markup.
- If the output folder input is not already under Knowledge/presentations, normalize it to a subfolder there.
- If key inputs are missing, ask only for the missing items.
- End with a short summary listing created files, render status, and the render command if applicable.
