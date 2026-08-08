# Create Instruction Infrastructure

- Add new instruction files to `./instructions/` with `.agent.md` extension.
- Keep instructions short, actionable, and focused on one workflow.
- Update `./instructions/main.agent.md` when adding or changing instructions.
- Use `Keywords:` sub-bullets to help route user requests to the correct instruction.
- Keep the catalog in `main.agent.md` aligned with the current files.
- For VS Code + Copilot, create wrapper prompts under `./.github/prompts/`.
- Keep wrappers simple: reference the instruction file and when to use it.
- Use `./instructions/creating-instructions.agent.md` as the bootstrap template.
