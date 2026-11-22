# How We Work — Group Project Playbook (OS300-GroupWork-CPUScheduling)

Read this fully before your first commit. It maps directly onto the lecturer's
marking rules, so following it protects your individual 40 marks.

## What we are building

CPU scheduling simulator (Option 1) in **Python**: reads process CSVs, runs
every algorithm on the same input, prints step-by-step Gantt timelines and one
comparison table, and shows matplotlib charts. The user can change the quantum,
CS cost and MLFQ quanta while it runs.

| Module | Algorithms | Owner (fill in) |
|--------|------------|-----------------|
| Module 1 | FCFS, SJF, SRTF | Ako-Nnubeng Frederick (@I-fredericks) — initial implementation |
| Module 2 | Round Robin, Priority + aging | TODO: member 2 |
| Module 3 | MLFQ, context-switch cost | TODO: member 3 |
| Shared | loader, compare table, charts, CLI, README, report | split — record in commits |

Current state: a complete working implementation with 15 passing unit tests
already exists on `main`. That is the **starting skeleton**: each module owner
must now *own* their module — read every line, be able to explain it live,
improve/extend it, add their own tests, and make their commits on it. The
report must disclose how AI tools were used, and every member must be able to
explain any part in the viva.

## One-time setup per member

```bash
git clone https://github.com/I-fredericks/OS300-GroupWork-CPUScheduling.git
cd OS300-GroupWork-CPUScheduling
git config user.name "Your Full Name"          # real name — graded
git config user.email "your student email"     # student email — graded
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest            # must show 15 passed before you touch anything
```

Branch names: `module1-fcfs-sjf-srtf`, `module2-rr-priority`, `module3-mlfq-cs`,
`shared-<thing>`.

## The weekly loop (this creates the graded commit history)

1. `git switch -c <branch>` from latest `main`.
2. Work in small steps; commit often with clear messages:
   `add SRTF preemption tie-break`, `extend module 2 aging test`, not `update`.
3. Before every push: `pytest` green.
4. Push and open a **Pull Request** into `main`; a different member reviews and
   merges. Never merge your own PR.
5. Never `git push --force` on `main`.

**Marking thresholds**: 10+ meaningful commits per member, spread over **3+
different weeks**. One giant end-of-deadline commit scores as one commit.

## Suggested schedule (adjust dates in the group chat)

- **Week 1** — everyone: setup above; owners read their module end to end and
  open their branch; each adds 2–3 tests with their own hand-worked examples.
- **Week 2** — owners extend their modules (e.g. module 2: changeable quantum
  demo path; module 3: CS-cost comparison on all inputs); shared: polish
  charts; everyone keeps committing.
- **Week 3** — comparison runs on all three inputs; screenshots for the report;
  report sections drafted per owner.
- **Week 4** — report assembly, evidence files, then film the video in one
  take; final zip.

## Report (6–10 pages, group mark)

Design decisions, results tables + charts from `inputs/test1..3`, comparison
discussion (SRTF wins on our inputs; why), what each member did, and an AI-tools
disclosure paragraph. Owners draft their own module's section.

## Video (15 of the group's marks — follow the rules exactly)

One continuous 12–18 min recording, **all members physically in frame**, no
cuts. Keep a visible clock with seconds the whole time. Sequence: ID + name +
index number each (first 60s) → one member reads date + group number → each
owner presents their module 3–4 min (concept, code walkthrough, live run) →
**live parameter change on camera** (e.g. `q4` then rerun and explain why the
table changed) → comparison conclusion → each member asks another one question.

## Submission (zip: OS300_GroupWork_CPUScheduling.zip)

```bash
git shortlog -sne                                    # screenshot -> GroupWork_shortlog.png
git log --all --pretty=format:"%h | %an | %ae | %ad | %s" --date=iso > GroupWork_gitlog.txt
```

Plus GitHub Insights → Contributors screenshot (`GroupWork_contributors.png`),
`GroupWork_members.txt`, `GroupWork_repo.txt` (link + submitted commit hash),
report PDF, and the video. The repo at the submitted hash is what gets marked —
commits after the deadline are ignored.
