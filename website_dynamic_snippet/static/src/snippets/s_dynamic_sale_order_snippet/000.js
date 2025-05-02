/** @odoo-module **/
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector: '.categories_section',
    disabledInEditableMode: false,
    events: {
        'click .load-more-button': '_onLoadMoreClick',
    },

    init() {
        this._super(...arguments);
        this.orm = this.bindService("orm");
        this.offset = 0;
        this.limit = 10;
    },

    async willStart() {
        await this.loadCategories();
    },

    async loadCategories() {
        if(this.$target[0].dataset.setLayout === 'list'){
            this.layout = 'list';
        } else {
            this.layout = 'grid';
            this.limit = 9;
        }
        const domain = this.$target[0].dataset.confirmOrderOnly === 'true' ? [['state', '=', 'sale']] : [];
        const result = await this.orm.searchRead(
            'sale.order',
            domain,
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
                { result: result, layout: this.layout },
            );

            const newTableRows = content.querySelectorAll('.list_sale_order > tbody > tr');
            const existingTableBody = this.el.querySelector('.list_sale_order > tbody');

            const newCardCols = content.querySelectorAll('.card_sale_order > .col-md-4');
            const existingCardWrapper = this.el.querySelector('.card_sale_order');

            if (this.offset === 0) {
                this.el.innerHTML = '';
                this.el.appendChild(content);
            } else {
                if (existingTableBody && newTableRows.length) {
                    newTableRows.forEach(row => existingTableBody.appendChild(row));
                }

                if (existingCardWrapper && newCardCols.length) {
                    newCardCols.forEach(card => existingCardWrapper.appendChild(card));
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
