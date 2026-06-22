from . import models

from odoo import Command


def add_tags(env):
    tags = []
    for i in range(10):
        tags.append(
            {
                "name": f"tag_{i + 1}",
                "color": i,
            }
        )

    env["task.manager.tags"].create(tags)


def _pre_init_hook(env):
    query = """
    DO $$
    DECLARE
        i INT;
        new_partner_id INT;
    BEGIN
        FOR i IN 0..9 LOOP
            INSERT INTO res_partner (name, phone, company_id, active, type)
            VALUES ('user_' || i, '0987654321', 1, true, 'contact')
            RETURNING id INTO new_partner_id;

            INSERT INTO res_users (login, partner_id, company_id, active, notification_type)
            VALUES ('user_' || i || '@example.com', new_partner_id, 1, true, 'email');
        END LOOP;
    END $$;
    """
    env.cr.execute(query)


def remove_users_with_mobile_number(env):
    target_logins = [f"user_{i}@example.com" for i in range(10)]
    users_to_remove = env["res.users"].search([("login", "in", target_logins)])

    if users_to_remove:
        partner_records = users_to_remove.partner_id
        users_to_remove.unlink()
        partner_records.unlink()
