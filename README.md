# Rick's crew (n8n jobs + free AI "brain switch") 🧪

The scheduled side of a home AI crew: each crew member is an [n8n](https://n8n.io) workflow that wakes up on a schedule,
collects facts from the crew API ([crew-dashboard](../../../crew-dashboard)), asks an AI to write a short in-character report,
and delivers it (daily note, notification, spoken aloud).

- `make_workflows.py` generates the n8n workflows into `workflows/` from one list of crew members (persona, schedule,
  model). Edit the list, run it, import with `n8n import:workflow --separate --input=/workflows`.
- `compose.yml` runs n8n (127.0.0.1 only).
- `apps/compose.yml` runs the free self-hosted apps the crew uses: Open WebUI, Open Notebook, Audiobookshelf, File Browser,
  FreshRSS, Forgejo, Stirling PDF, LibreTranslate, Kiwix (offline library), an offline map viewer and the brain switch.
- `apps/brain-switch/config.yaml` is a [LiteLLM](https://github.com/BerriAI/litellm) config: one OpenAI-style address
  (`127.0.0.1:4000/v1`) with jobs like `free-chat`, `free-smart`, `free-coder`. Each job tries free API tiers in order (Groq,
  Gemini, Mistral Codestral, OpenRouter `:free`, Cloudflare Workers AI, NVIDIA NIM, Ollama Cloud) and falls back to local [Ollama](https://ollama.com)
  models when offline. Put your own keys in an env file (`GROQ_API_KEY=...`); none are included.

Paths assume an external drive at `/run/media/$USER/OmarchyExt1`; change them in the compose files.

## License

MIT. Built by Rabbid Raccoon with Claude. Use it, change it, share it.
