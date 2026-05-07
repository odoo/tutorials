# Demo Data

This addon ships optional demo data in `data/` (loaded when demo data is enabled for the database).

## Medicines

File: `data/demo_medicines.xml`

Creates:
- A sample category: **Painkiller** (`pharmacy.category`)
- Sample medicines (`pharmacy.medicine`) covering different license categories:
  - Paracetamol 500mg (white)
  - Amoxicillin 500mg (blue)
  - Morphine Sulphate (green)

The demo expiry dates are intentionally mixed so you can test the *Fresh / Expiring Soon / Expired* badges depending on the current date.

## Patients

File: `data/demo_patients.xml`

Creates three sample patients (`pharmacy.patient`) assigned to:
- `base.user_admin` (Administrator)

