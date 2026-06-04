# Chapter 7 - Relations Between Models

- This chapter makes `awesome_estate` multi-model.
- The property record links to type, buyer, salesperson, tags, and offers.
- The important part is the relation itself, not extra business logic.

---

## What Chapter 7 adds

### Property type
- Model: `awesome.estate.property.type`
- Required field: `name`
- Property field: `property_type_id` (`Many2one`)
- Add the list, form, action, and menu for property types.

### Buyer and salesperson
- Buyer field: `buyer_id`
  - Model: `res.partner`
  - Should not be copied on duplicate
- Salesperson field: `salesperson_id`
  - Model: `res.users`
  - Default: current user (`self.env.user`)

### Tags
- Model: `awesome.estate.property.tag`
- Required field: `name`
- Property field: `tag_ids` (`Many2many`)
- Add the tag list, form, action, and menu.

### Offers
- Model: `awesome.estate.property.offer`
- Required fields:
  - `price`
  - `status`
  - `partner_id`
  - `property_id`
- Property field: `offer_ids` (`One2many`)
- Add the offer list and form views.
- Add the offers tab inside the property form.

---

## What the chapter has

### Many2one
- One record points to one other record.
- In this module:
  - one property has one type
  - one property has one buyer
  - one property has one salesperson

### Many2many
- Records can link to many other records on both sides.
- In this module:
  - one property can have many tags
  - one tag can be used on many properties

### One2many
- One2many is the inverse of a Many2one.
- In this module:
  - one property has many offers
  - each offer belongs to one property

### Important rule
- A `One2many` must always have a real inverse `Many2one` field on the child model.

---

### XML
- Load the new XML files in `__manifest__.py`.
- Add the views for:
  - property type
  - property tag
  - property offer
  - property form update

### Security
- Add ACL rows for:
  - property type
  - property tag
  - property offer

---

## Notes

- `property_type_id` stores the selected type for each property.
- `tag_ids` stores reusable labels.
- `offer_ids` shows the offers linked to one property.
- `buyer_id` is `copy=False`.
- `status` on offers is `copy=False`.
- `salesperson_id` defaults to `self.env.user`.

---

## What I explored

- Python defines the model.
- XML defines the UI.
- Relations make the module more realistic.
- `Many2one`, `Many2many`, and `One2many` are the main tools for this chapter.
- Offers belong inside the property form.
- Tags and property types need their own views and menus.

---

## Summary

- Chapter 7 is about linking models together.
- The property becomes the center record.
- Type, buyer, salesperson, tags, and offers all connect to it.
- The goal is to understand the relation types and wire them cleanly.
