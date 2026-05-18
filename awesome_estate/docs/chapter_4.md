# Security 

- module: `awesome_estate`
- model: `awesome_estate.property`
- ACL file: `tutorials/awesome_estate/security/ir.model.access.csv`
- manifest entry: `data: ['security/ir.model.access.csv']`

If a model has no access rights, Odoo treats it as inaccessible and prints a warning in the logs.

---

1. **Access rights (ACLs)**  
   Model-level permissions:
   - read
   - write
   - create
   - unlink

2. **Groups**  
   ACLs are assigned to a group like `base.group_user`.

3. **Record rules**  
   Used later to limit which records a group can see or edit.

For Chapter 4, the important part is ACLs.

---

## ACL file format

File: `tutorials/awesome_estate/security/ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_awesome_estate_property,access_awesome_estate_property,model_awesome_estate_property,base.group_user,1,1,1,1
```

### What each part means

- `id`  
  External ID of the access rule record.

- `name`  
  Human-readable name.

- `model_id:id`  
  Model the rule applies to.  
  For `awesome_estate.property`, the value is:
  - `model_awesome_estate_property`

- `group_id:id`  
  Group that gets the permissions.  
  Here:
  - `base.group_user`

- `perm_read`  
  Can read records.

- `perm_write`  
  Can edit records.

- `perm_create`  
  Can create records.

- `perm_unlink`  
  Can delete records.  
  In Odoo, `unlink` means delete.

### What this row gives

This row gives internal users in `base.group_user` full access to the model:

- read = 1
- write = 1
- create = 1
- unlink = 1

---

## Manifest wiring

File: `tutorials/awesome_estate/__manifest__.py`

```python
'data': ['security/ir.model.access.csv'],
```

Why this matters:

- Odoo only loads security data files if they are declared in the manifest.
- The file is loaded when the module is installed or upgraded.

---
