/** @odoo-module **/
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector: '.categories_section',

    init() {
        this._super(...arguments);
        this.orm = this.bindService("orm");
        this.offset = 0;
        this.limit = 10;
    },

    async willStart() {
        await this.loadCategories();
    },

    events: {
        'click .load-more-button': '_onLoadMoreClick',
    },

    async loadCategories() {
        const result = await this.orm.searchRead(
            'sale.order',
            [],
            ['id', 'name', 'partner_id', 'amount_total', 'state'],
            {
                offset: this.offset,
                limit: this.limit,
                order: 'id ASC',
            }
        );

        if (result && result.length) {
            const content = await renderToElement(
                'website_dynamic_snippet.sale_order_snippet',
                { result: result }
            );

            if (this.offset === 0) {
                this.el.innerHTML = '';
                this.el.appendChild(content);
            } else {
                const newRows = content.querySelectorAll('tbody > tr');
                const existingTbody = this.el.querySelector('tbody');
                if (existingTbody) {
                    newRows.forEach(row => {
                        existingTbody.appendChild(row);
                    });
                }
            }

            this.offset += result.length;
        } else {
            const loadMoreButton = this.el.querySelector('.load-more-button');
            if (loadMoreButton) {
                loadMoreButton.style.display = 'none';
            }
        }
    },

    async _onLoadMoreClick(ev) {
        ev.preventDefault();
        await this.loadCategories();
    },
});
