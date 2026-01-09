---
id: 1
title: Create hackathon todo constitution
stage: constitution
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Claude
command: sp.constitution
labels: [constitution, spec-driven-development, security]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - null
---

## Prompt

You are an expert full-stack architect and specification authority.

Create a project constitution for a Spec-Driven Development monorepo project using Spec-Kit Plus.

Project Name: hackathon-todo
Phase: Phase II – Full-Stack Web Application

The constitution MUST:
- Enforce Spec-Driven Development strictly
- Disallow implementation without approved specs
- Define security boundaries clearly
- Define frontend vs backend responsibilities
- Define authentication model using Better Auth + JWT
- Define database ownership and access rules
- Define monorepo structure rules
- Define API security rules
- Define coding standards and conventions

Technical Stack (MANDATORY):
- Frontend: Next.js 16+ (App Router, TypeScript, Tailwind CSS)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (frontend) with JWT tokens
- Authorization: JWT verification in FastAPI
- Spec System: Spec-Kit Plus

Authentication Rules:
- Better Auth runs ONLY in frontend
- Backend must NEVER trust user_id from URL without JWT validation
- JWT must be verified using shared secret (BETTER_AUTH_SECRET)
- Every API request must include Authorization: Bearer <token>
- Backend extracts user identity ONLY from JWT
- Backend enforces task ownership on every operation

API Rules:
- All routes under /api/
- RESTful conventions
- JSON only
- Stateless authentication
- Return 401 for missing/invalid tokens
- Return 403 for unauthorized access

Database Rules:
- users table is managed logically by Better Auth
- tasks table must reference users.id
- All queries must be filtered by authenticated user

Spec Rules:
- All features must have:
  - User stories
  - Acceptance criteria
- S

## Response snapshot

Created comprehensive project constitution for hackathon-todo project with specific sections for:

1. Core Principles:
   - Spec-Driven Development (NON-NEGOTIABLE)
   - Security-First Architecture
   - Test-First Development (NON-NEGOTIABLE)
   - Frontend-Backend Separation
   - Authentication and Authorization Integrity
   - API-First Design

2. Security Boundaries and Responsibilities:
   - Frontend vs Backend responsibilities
   - Authentication model using Better Auth + JWT
   - Database ownership and access rules

3. Technical Stack Requirements:
   - Mandatory technologies (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth)
   - Coding standards and conventions

4. API Security Rules:
   - Endpoint requirements and authentication enforcement

5. Database Rules:
   - Schema requirements and access control

6. Spec Rules:
   - Specification requirements and quality standards

7. Development Workflow:
   - Code review process and quality gates

8. Governance:
   - Amendment process and compliance review

Updated related templates to align with the constitution:
- plan-template.md: Added constitution check gates
- spec-template.md: Added security and authentication requirements section
- tasks-template.md: Updated foundational tasks to include security/auth implementation

## Outcome

- ✅ Impact: Created complete project constitution and aligned templates
- 🧪 Tests: Not applicable
- 📁 Files: Updated .specify/memory/constitution.md, .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- 🔁 Next prompts: Project constitution is established, ready for feature specifications
- 🧠 Reflection: Constitution enforces security-first architecture and spec-driven development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All requirements met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin creating feature specifications following the constitution