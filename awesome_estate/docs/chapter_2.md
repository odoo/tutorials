# Chapter 2

## Module dependency

`base`

- My module needs Odoo core to be installed first.

### Where `base` lives in this repo

`community/odoo/addons/base/`

### What `base` provides

- Fundamental UI framework pieces and security bootstrap.
- Core records like languages, users, partners, currencies, companies, and countries.
- Base security, group, and access basics (Chapter 4).

### Why my module depends on it

Without `base`, Odoo is missing the required core models, configuration, and security layer, so my module cannot install safely.

### Notes

`application: true` suggests that this is an installable app, and `false` means it is a module.
