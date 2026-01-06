import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";


registry.category("web_tour.tours").add('estate_tour', {
    steps: () => [{
    trigger: '.o_app[data-menu-xmlid="estate.menu_root"]',
    content: _t('Start selling your properties from this app!'),
    }],
});
