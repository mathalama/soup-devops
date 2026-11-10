# Soup release engineering exercise

## Design
Build a small dependency-free greeting CLI. Treat source tests and installed-artifact tests as different evidence. Inject four independent incidents into disposable project copies, never into the release source. Preserve all failed Actions runs.

## Ordered work
1. Define CLI behavior with unittest; implement Python >=3.10 package.
2. Build wheel and sdist. Install each outside the source tree and exercise the console command.
3. Reproduce Python 3.10 import, Windows import, omitted package data, and broken entry-point failures. Compare naive and hardened runs for each.
4. Add Docker and Actions matrix, then isolated OIDC publication of the exact tested artifacts.
5. Close supply-chain gaps: locked tools, minimum permissions, no PR publication, current-run artifact identity, tag/version parity, no cache in release verification.
6. Gather real red/green run URLs, design GPU release/nightly checks and cost model, write <=2 page note and AI disclosure.

## Risks / external setup
- Docker CLI exists but Docker Desktop engine is currently unavailable.
- GitHub authenticated as mathalama; remote creation/push still pending user instruction.
- TestPyPI account and trusted-publisher configuration have not been verified.
- No GPU resources will be rented for a design-only requirement.
- Local Windows Python is 3.10.11. Other interpreters and Linux/macOS need additional execution environments.

## Acceptance
Each incident must pass naive checks and fail a relevant hardened gate for the intended cause. Fixed source must pass artifact installation on the declared OS/Python matrix. Published version must match its tag. All incomplete verification must remain explicit.
