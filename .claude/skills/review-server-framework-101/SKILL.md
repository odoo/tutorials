---
description: Review a newcomer's Odoo PR for the Server Framework 101 tutorial.
argument-hint: "[PR URL or number]"
allowed-tools: Read, Bash, Grep, WebFetch
---

The Server Framework 101 tutorial asks newcomers to develop a module from scratch to manage a real
estate business. They can push their changes at any time without having completed all the chapters.
Fetch the tutorial's instructions from
https://odoo.com/documentation/latest/developer/tutorials/server_framework_101.html.

Review a newcomer's PR the way the tutorial's regular reviewers do: **concise**, specific, pointing
at the convention being violated. The goal is to provide a few relevant pointers to the author, not
drown them in comments until the PR is perfect.

## How to review

1. **Read every changed file in full**, XML and CSV included. Only review this tutorial's modules
   (`estate`, `estate_account`, ...). Ignore files from other tutorials (e.g. `awesome_owl`,
   `awesome_dashboard`) and commits that only touch them: don't review them or comment on them.
2. **Go through the checklist**, then hunt for the bugs listed below. Don't ask for something a 
   later chapter introduces.
3. **When you find a pattern, search for it everywhere** (every action method, every view, every
   model) and report it only once.
4. **Tone:** short, name the convention, state the fix.

## Bugs to look for in any file

These have no checklist entry; you only find them by reading.

- A reference to something that doesn't exist: a field, an XML id, an action, a filter name that
  doesn't match the `search_default_*` key.
- A condition that can never be true, given the field's declared `Selection` values.
- A side effect (creating an invoice, writing another record) that runs before the validation that
  should gate it.
- A method that reads `self.field` with no loop and no `ensure_one()` and crashes on several
  records; a compute that skips records (early `return` in the loop) or has no `@api.depends`.
- A `write()`/`create()` value of the wrong shape: a dict assigned to a Many2one (it takes an id),
  or bare ids/dicts for a One2many/Many2many (they take `Command`s).
- Copy-paste leftovers: labels, context keys or text from an unrelated view; stray characters.
- A test that can't pass as written (wrong exception class) or never exercises the success path.

## Checklist

### From the start

- **[should fix]** Keep CI green before asking for review.
- **[should fix]** One commit per chapter; squash fixups into the commit they fix.
- **[should fix]** Commit messages: `[TAG] module: imperative description` (`[ADD]` for a new
  module, `[IMP]` after); the body says *why*.
- **[should fix]** Dotted model names (`estate.property`) with a matching class (`EstateProperty`).
  *(from the first model)*
- **[nit]** End every file with a single newline.
- **[should fix]** Don't commit editor/tooling config (`.vscode`, `.editorconfig`, `ruff.toml`) or files
  outside your module. Other tutorials' modules don't count here; ignore them.
- **[nit]** Imports: stdlib/third-party, then `odoo`, then `odoo.addons`; alphabetized.
- **[nit]** Don't restate manifest defaults (`version`, `installable`, empty `demo`).
- **[nit, soft]** Pass field constructor arguments by keyword (`comodel_name=`, `string=`).

### By chapter

- **Ch. 4 Security**
  - **[should fix]** 20.0 uses `security/ir.access.csv` (`id,name,model_id,group_id/id,operation,domain`),
    not `ir.model.access.csv`; the old file won't load. Ids follow `access_<model>_<group>`.
  - **[should fix]** Security file first in the manifest `data` list, menus last; files load in order.
- **Ch. 5 Defaults**
  - **[blocking]** `default=` must be callable (`lambda self: ...`), never a bare expression such as
    `fields.Date.today() + ...`. A bare one is computed once at server start, so every new record
    gets a stale value. A module-level constant holding the computed value is the same bug.
  - **[should fix]** Selection keys are snake_case (`offer_received`, not `offer received`).
  - **[nit]** Use `fields.Date`/`fields.Datetime` helpers, not `datetime`/`relativedelta`.
- **Ch. 6 Views**
  - **[should fix]** `<list>`, not `<tree>` (20.0 no longer recognises `<tree>`).
  - **[nit]** Set a field's `string=` once on the model; don't repeat it in every view.
- **Ch. 7 Relations**
  - **[should fix]** `_id` suffix for Many2one, `_ids` for One2many/Many2many.
- **Ch. 8 Compute & onchange**
  - **[should fix]** `_compute_*` / `_onchange_*` prefixes.
  - **[should fix]** `@api.depends` lists every field the compute reads (including `create_date`),
    and the compute assigns every record.
  - **[should fix]** Model order: private attrs → fields → SQL constraints → compute/inverse/search
    → selection → constrains/onchange → CRUD → actions → business methods.
  - **[nit]** `max(x.mapped('f'), default=0)` rather than an if/else.
  - **[nit, soft]** A descriptive loop variable can read better than `record`.
- **Ch. 9 Actions**
  - **[blocking]** Never fail silently. On a failed precondition `raise`; don't `return False`, and
    don't build a `UserError(...)` without raising it. Check every action method.
  - **[should fix]** Wrap error messages in `self.env._()`.
  - **[nit]** Check a condition across `self` once and assign in bulk instead of looping per record.
- **Ch. 10 Constraints**
  - **[should fix]** `float_compare`/`float_is_zero`, not `==`/`<` on floats.
  - **[should fix]** `models.Constraint(...)`, not `_sql_constraints` (20.0 ignores the old list).
- **Ch. 12 Inheritance**
  - **[should fix]** Write `create()` for a list: `@api.model_create_multi`, iterate `vals_list`.
    Blocking if the body treats `vals` as a single dict.
  - **[should fix]** No `browse`/`search` inside the loop; batch before it.
  - **[should fix]** Don't assume keys exist in `vals` (`vals['property_id']`); use `.get()`.
- **Ch. 13 Other modules**
  - **[nit]** `auto_install: True` on a glue module that bridges two independent modules (e.g.
    `estate_account` depends on `estate` and `account`).

## Output format

Present findings in a table. Group by file. One line per finding, starting with its location as
`Line <line_no>` (or `Lines <start-end>`), using line numbers from the PR's head version of the
file. A commit-level finding names the commit's short hash instead.

- **blocking**: breaks functionality or install; fix before merge.
- **should fix**: a convention a reviewer will always flag.
- **nit**: style; optional.
- **good**: something done well; optional, at most two or three across the whole review.

Report a repeated pattern once, with two or three locations and "apply everywhere", rather than
listing every line.

Put each **good** point in its file's table, as its own row with its own location, after that
file's findings, so each one can be posted as a separate comment. A file with only good points
still gets a table.
