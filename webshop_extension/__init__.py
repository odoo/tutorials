from . import models

def post_init_hook(env):
    languages_to_activate = ['da_DK', 'sv_SE']
    
    for lang_code in languages_to_activate:
        # with_context(active_test=False) allows us to find records even if they are inactive by default odoo will ignore them
        lang = env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)], limit=1)
        if lang:
            lang.write({'active': True})
