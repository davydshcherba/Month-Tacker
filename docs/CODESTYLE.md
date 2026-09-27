# Code Style & Contribution Guidelines

**Stack:** FastAPI · Python · React · TypeScript
**Purpose:** Keep the codebase consistent, readable, maintainable, and
easy to review.

These rules apply to all contributions unless a project-specific
decision explicitly overrides them. Prefer simple, explicit solutions
over clever or unnecessarily abstract code.

------------------------------------------------------------------------

## 1. Core Principles

-   **Readability first.** Code is read more often than it is written.
-   **Be consistent.** Follow existing patterns before introducing new
    ones.
-   **Keep changes focused.** One change should solve one clearly
    described problem.
-   **Make behavior explicit.** Avoid hidden side effects and surprising
    defaults.
-   **Use types.** Add useful type annotations on both backend and
    frontend.
-   **Validate at boundaries.** Treat incoming requests, environment
    variables, and external data as untrusted.
-   **Do not commit secrets, generated files, or unrelated formatting
    changes.**

## 2. Repository Structure

Use a clear separation between backend and frontend. Adapt folder names
to the existing repository, but keep responsibilities distinct.

``` text
project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── db/
│   │   └── main.py
│   ├── tests/
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── services/
│   │   ├── types/
│   │   └── main.tsx
│   ├── public/
│   └── package.json
├── docs/
├── .gitignore
└── README.md
```

### Folder responsibilities

-   `api/routes/`: HTTP endpoints, dependency wiring, request/response
    handling.
-   `schemas/`: Pydantic request and response models.
-   `models/`: database models and persistence entities.
-   `services/`: business logic and orchestration.
-   `repositories/`: database access patterns, if the project uses this
    layer.
-   `core/`: configuration, security, logging, shared application setup.
-   `components/`: reusable UI components.
-   `features/`: feature-oriented React code (screens, feature
    components, hooks, API calls).
-   `services/`: frontend API client and integrations.
-   `types/`: shared frontend TypeScript types that are not
    feature-specific.

Avoid creating layers or folders without a real need. Do not move files
just for the sake of matching this example.

------------------------------------------------------------------------

## 3. General Naming Conventions

  Item                             Convention                               Example
  -------------------------------- ---------------------------------------- ---------------------
  Python modules                   `snake_case`                             `user_service.py`
  Python functions/variables       `snake_case`                             `get_user()`
  Python classes                   `PascalCase`                             `UserService`
  Constants                        `UPPER_SNAKE_CASE`                       `MAX_RETRIES`
  React components                 `PascalCase`                             `UserProfile.tsx`
  React hooks                      `camelCase`, `use` prefix                `useCurrentUser.ts`
  TypeScript functions/variables   `camelCase`                              `fetchUser()`
  TypeScript types/interfaces      `PascalCase`                             `UserResponse`
  CSS classes                      project convention; prefer clear names   `user-card`
  Environment variables            `UPPER_SNAKE_CASE`                       `DATABASE_URL`
  Git branches                     lowercase kebab-case                     `feat/user-profile`

Names should describe intent. Avoid unclear abbreviations such as `usr`,
`tmp2`, or `do_stuff`, except for conventional short loop variables.

------------------------------------------------------------------------

## 4. Python & FastAPI Style

### 4.1 Formatting and linting

-   Use **4 spaces** for indentation; never tabs.
-   Follow **PEP 8**.
-   Keep lines reasonably short; target **88--100 characters** where
    practical.
-   Use a formatter and linter consistently (recommended: Ruff).
-   Do not manually reformat code differently from the project's
    configured formatter.
-   Remove unused imports, variables, and dead code.

Recommended tools:

-   `ruff format` --- formatting.
-   `ruff check` --- linting.
-   `mypy` or Pyright --- optional static type checking, depending on
    project setup.
-   `pytest` --- tests.

### 4.2 Type annotations

Annotate function parameters and return values, especially public
functions and service methods.

``` python
def get_display_name(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name}".strip()
```

Prefer specific types over `Any`. Use `Any` only when the value is
genuinely dynamic and explain why when it is not obvious.

Use modern built-in generics:

``` python
def get_ids() -> list[int]:
    return [1, 2, 3]
```

Use `X | None` for optional values when supported by the project's
Python version.

### 4.3 FastAPI route design

-   Keep route handlers thin: validate input, call the relevant service,
    return the result.
-   Put business rules in services, not in route functions.
-   Use `APIRouter` to group endpoints by domain.
-   Use explicit response models for public endpoints.
-   Use appropriate HTTP methods and status codes.
-   Use dependency injection for shared resources such as database
    sessions and authenticated users.
-   Do not expose database models directly as public API contracts
    unless deliberately designed that way.

``` python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse.model_validate(user)
```

Use the dependency style already adopted by the project. Do not mix
dependency patterns without a reason.

### 4.4 Pydantic schemas

-   Use Pydantic models to validate and document request and response
    data.
-   Name schemas by purpose, for example `UserCreate`, `UserUpdate`,
    `UserResponse`.
-   Separate input schemas from output schemas when their fields or
    trust boundaries differ.
-   Do not accept server-controlled fields (such as ownership, role, or
    internal IDs) from clients unless explicitly required and
    authorized.
-   Configure ORM/object attribute reading according to the installed
    Pydantic version and project conventions.

### 4.5 Async and database access

-   Use `async def` when the route or call chain performs asynchronous
    I/O.
-   Do not call blocking I/O directly inside an async function. Use an
    async library or an appropriate threadpool strategy.
-   Do not add `await` to synchronous functions.
-   Keep database transactions clear and bounded.
-   Avoid N+1 queries; load related data intentionally.
-   Do not silently swallow database exceptions.

### 4.6 Errors and logging

-   Raise meaningful, expected application errors and map them to
    suitable HTTP responses.
-   Never return raw stack traces or internal exception details to
    clients in production.
-   Do not use exceptions for ordinary control flow when a normal
    conditional is clearer.
-   Use the project's logger instead of `print()` for application
    diagnostics.
-   Do not log passwords, access tokens, API keys, session cookies, or
    sensitive personal data.
-   Include useful context in logs without exposing secrets.

### 4.7 Configuration and security

-   Read configuration from environment variables or the project's
    settings system.
-   Keep `.env` files out of version control; commit `.env.example` with
    placeholder values only.
-   Never hardcode credentials, signing keys, or production URLs
    containing secrets.
-   Validate and normalize external input.
-   Enforce authorization on the server, not only in the frontend.
-   Use password hashing and established authentication/security
    libraries; do not invent cryptography.
-   Configure CORS with explicit allowed origins for deployed
    environments.
-   Keep dependencies updated through the project's normal review
    process.

------------------------------------------------------------------------

## 5. React & TypeScript Style

### 5.1 TypeScript

-   Prefer TypeScript for application code.
-   Avoid `any`; use `unknown` for values that must be narrowed before
    use.
-   Define explicit types for API responses, component props, and
    important state.
-   Prefer inference for obvious local variables; do not add noisy
    redundant annotations.
-   Use `type` or `interface` consistently with the project's existing
    convention.
-   Avoid unsafe type assertions. If one is necessary, keep it narrow
    and document the reason.

``` tsx
type UserCardProps = {
  name: string;
  email?: string;
  onSelect?: () => void;
};

export function UserCard({
  name,
  email,
  onSelect,
}: UserCardProps) {
  return (
    <button type="button" onClick={onSelect}>
      <strong>{name}</strong>
      {email && <span>{email}</span>}
    </button>
  );
}
```

### 5.2 Components

-   Use function components.
-   Use `PascalCase` for component names and component files.
-   Keep components focused on one UI responsibility.
-   Extract repeated or complex logic into hooks or utilities.
-   Keep props explicit and minimal.
-   Do not create abstractions for one-off code unless they improve
    clarity.
-   Avoid deeply nested conditional JSX; use early returns or named
    variables when clearer.
-   Use semantic HTML and accessible labels, keyboard behavior, and
    focus states.

### 5.3 Hooks and state

-   Follow the Rules of Hooks: call hooks at the top level of components
    or custom hooks.
-   Name custom hooks with the `use` prefix.
-   Keep state close to where it is used.
-   Avoid duplicating derived state; calculate it from existing state
    when practical.
-   Use effects for synchronizing with external systems, not as a
    default place for ordinary calculations.
-   Clean up subscriptions, listeners, and other effect resources when
    needed.
-   Do not suppress effect dependency warnings without a documented
    reason.

### 5.4 Styling

-   Follow the styling system already used by the project (CSS Modules,
    Tailwind, styled-components, etc.).
-   Do not introduce a second styling system without agreement.
-   Avoid inline styles for large or reusable style definitions.
-   Keep responsive behavior and accessibility in mind.
-   Use design tokens or shared variables for repeated colors, spacing,
    and typography when available.
-   Avoid global selectors that unintentionally affect unrelated
    components.

### 5.5 Frontend data and API calls

-   Keep API access in a shared client or feature service rather than
    scattering raw `fetch()` calls across components.
-   Type request and response data.
-   Handle loading, success, empty, and error states.
-   Do not assume a request succeeded until its result is checked.
-   Avoid storing secrets in frontend environment variables; frontend
    variables are generally exposed to the browser.
-   Do not trust client-side validation as a replacement for backend
    validation.
-   Cancel or ignore stale requests when appropriate to prevent outdated
    UI updates.

------------------------------------------------------------------------

## 6. API Contract

-   Use resource-oriented, predictable endpoint names.
-   Use plural nouns for collections where practical: `/users`,
    `/projects`.
-   Use path parameters for resource identity and query parameters for
    filtering, sorting, or pagination.
-   Keep request and response shapes consistent.
-   Document non-obvious behavior, validation constraints, and error
    responses.
-   Treat OpenAPI as part of the API contract.
-   Coordinate breaking API changes with frontend usage and update both
    sides in the same change when possible.
-   Use a consistent date/time format (prefer ISO 8601) and document
    timezone expectations.
-   Do not return fields the client does not need, especially internal
    or sensitive fields.

Example:

``` text
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/{project_id}
PATCH  /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}
```

Versioning (`/api/v1`) should be used if it matches the project's
release and compatibility strategy.

------------------------------------------------------------------------

## 7. Testing

### Backend

-   Use `pytest`.
-   Test business logic separately from HTTP routing where practical.
-   Cover successful behavior, validation failures, authorization, and
    expected error cases.
-   Use fixtures for repeatable setup and cleanup.
-   Mock external services at their boundaries; do not mock every
    internal function.
-   Tests must be deterministic and must not depend on production
    services or real credentials.

### Frontend

-   Use the project's chosen test framework (for example, Vitest and
    React Testing Library).
-   Test user-visible behavior rather than implementation details.
-   Cover important states: loading, empty, error, and success.
-   Prefer accessible queries such as role and label.
-   Mock network boundaries consistently.

### General

-   Add or update tests when behavior changes.
-   Fix flaky tests rather than rerunning them until they pass.
-   Do not remove a test just to make a change pass without explaining
    the reason.
-   Run relevant checks before opening a PR.

------------------------------------------------------------------------

## 8. Git Branching

Use short-lived branches based on the main integration branch (usually
`main`).

### Branch naming

Format:

``` text
<type>/<short-description>
```

Allowed types:

  Type          Use
  ------------- -----------------------------------------------------
  `feat/`       New feature
  `fix/`        Bug fix
  `refactor/`   Code restructuring without intended behavior change
  `docs/`       Documentation-only changes
  `test/`       Test additions or changes
  `chore/`      Tooling, dependencies, maintenance
  `perf/`       Performance improvement
  `ci/`         CI/CD changes

Examples:

``` text
feat/user-authentication
fix/token-expiration
refactor/api-dependencies
docs/local-setup
test/project-service
chore/update-dependencies
```

Rules:

-   Use lowercase kebab-case.
-   Keep names short but meaningful.
-   Do not use spaces, personal names, or vague names like `updates` or
    `stuff`.
-   Create branches from the current `main`.
-   Keep branches focused and delete them after merging when
    appropriate.
-   Do not commit directly to `main` except for explicitly permitted
    repository maintenance.

------------------------------------------------------------------------

## 9. Commit Messages

Use **Conventional Commits**.

Format:

``` text
<type>(optional-scope): <description>
```

Examples:

``` text
feat(auth): add refresh token endpoint
fix(users): handle missing profile image
refactor(api): extract project service
docs: clarify local development setup
test(auth): cover expired access tokens
chore(deps): update fastapi
```

### Commit types

  Type         Meaning
  ------------ ------------------------------------------------------
  `feat`       Adds user-facing or functional capability
  `fix`        Fixes a bug
  `refactor`   Changes structure without changing intended behavior
  `docs`       Documentation changes
  `test`       Test-only changes
  `chore`      Maintenance or tooling
  `perf`       Performance improvement
  `ci`         CI/CD configuration
  `build`      Build system or packaging changes
  `style`      Formatting-only changes with no logic change

### Commit rules

-   Use the imperative mood: `add`, `fix`, `update`, not `added`,
    `fixed`, `updates`.
-   Keep the subject concise (ideally under 72 characters).
-   Do not end the subject with a period.
-   Describe what the commit changes, not what you were doing.
-   Keep each commit logically focused.
-   Use a body when context, reasoning, or trade-offs are not obvious.
-   Mark breaking changes with `!` and explain them in the body or
    footer.

Example breaking change:

``` text
feat(api)!: rename project owner field

BREAKING CHANGE: `owner` is now returned as `owner_id`.
Update clients that read the previous response field.
```

Avoid vague messages such as:

``` text
update
fix
changes
final
work
```

------------------------------------------------------------------------

## 10. Pull Requests

Before opening a PR:

-   [ ] The branch is up to date with the target branch.
-   [ ] The change has a clear, limited scope.
-   [ ] Relevant tests have been added or updated.
-   [ ] Formatting, linting, type checks, and tests pass.
-   [ ] No secrets, debug code, or unrelated files are included.
-   [ ] Documentation and API types are updated when needed.
-   [ ] The change has been tested locally where practical.

### PR title

Use the same style as commit messages:

``` text
feat(auth): add refresh token endpoint
```

### PR description template

``` markdown
## Summary
What changed and why?

## Changes
- ...
- ...

## Testing
- [ ] Backend tests
- [ ] Frontend tests
- [ ] Lint / format / type checks
- [ ] Manual verification (if applicable)

## Screenshots
Add screenshots for meaningful UI changes.

## Notes
Breaking changes, migration steps, risks, or follow-up work.
```

Keep PRs reviewable. If a change is large, split it into smaller
independent PRs when practical.

------------------------------------------------------------------------

## 11. Code Review

Reviewers should focus on:

1.  Correctness and expected behavior.
2.  Security, authorization, and data handling.
3.  Readability and maintainability.
4.  Tests and edge cases.
5.  Performance where relevant.
6.  Consistency with project conventions.

Review rules:

-   Be specific, respectful, and constructive.
-   Explain why a change is needed, not only what to change.
-   Distinguish blocking issues from suggestions.
-   Do not request stylistic changes that conflict with the repository's
    configured tools.
-   Authors should respond to comments and resolve threads when
    addressed.
-   Do not merge with unresolved blocking feedback.

------------------------------------------------------------------------

## 12. Dependencies and Generated Files

-   Add dependencies only when they provide clear value.
-   Prefer maintained, widely used packages that fit the stack.
-   Pin or lock dependencies using the project's existing
    package-management approach.
-   Explain unusual or security-sensitive dependencies in the PR.
-   Do not manually edit generated files when they can be regenerated
    from source.
-   Commit lockfiles when required by the package manager and project
    policy.
-   Do not commit virtual environments, build output, caches, local
    databases, or editor-specific files unless explicitly needed.

------------------------------------------------------------------------

## 13. Documentation

-   Update documentation when setup, configuration, API behavior, or
    developer workflows change.
-   Keep the README focused on project overview, prerequisites, setup,
    and common commands.
-   Document environment variables in `.env.example` or a dedicated
    configuration reference.
-   Add comments to explain *why* something is non-obvious, not to
    narrate every line.
-   Keep examples accurate and runnable where practical.

------------------------------------------------------------------------

## 14. Definition of Done

A change is ready to merge when:

-   It solves the stated problem and stays within scope.
-   The code follows these conventions and existing project patterns.
-   Inputs and permissions are validated at the appropriate boundaries.
-   Relevant tests pass and important edge cases are considered.
-   Linting, formatting, and type checks pass where configured.
-   API contracts and documentation are updated when necessary.
-   The PR explains the change, testing, and any risks.
-   No secrets, unrelated changes, or avoidable debug artifacts remain.

------------------------------------------------------------------------

## 15. Recommended Local Checks

Use the commands configured by the repository. These are examples, not
mandatory scripts; adjust them to match the actual project setup.

Backend:

``` bash
cd backend
ruff check .
ruff format --check .
pytest
```

Frontend:

``` bash
cd frontend
npm run lint
npm run typecheck
npm test
npm run build
```

If a script does not exist, do not assume it does---check
`pyproject.toml` and `package.json` and use the project's actual
commands.

**When in doubt:** follow the established pattern in the codebase, keep
the change small, and explain decisions that affect other contributors.
