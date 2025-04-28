/** @odoo-module **/
import { renderToElement } from "@web/core/utils/render";
import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";

class SaleOrderSnippet extends Interaction {
    static selector = ".categories_section";
    dynamicContent =  {
        ".load-more-button": {
            "t-on-click": this._onLoadMoreClick,
        }
    };

    setup() {
        this.orm = this.services.orm;
        this.layout = this.el.dataset.setLayout === 'list' ? 'list' : 'grid';
        this.offset = 0;
        this.limit = this.layout === 'list' ? 10 : 9;
    };

    async willStart() {
        await this.loadCategories();
    };

    async loadCategories() {
        const template = this.layout === 'list'
            ? 'website_dynamic_snippet.sale_order_snippet_list'
            : 'website_dynamic_snippet.sale_order_snippet_grid';

        const domain = this.el.dataset.confirmOrderOnly === 'true' ? [['state', '=', 'sale']] : [];
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
                template,
                { result: result },
            );
            const selector = this.layout === 'list' ? '.list_sale_order > tbody' : '.card_sale_order';
            const targetContainer = this.el.querySelector(selector);
            const newContentContainer = content.querySelector(selector);

            if (this.offset === 0) {
                this.el.replaceChildren(content);
            } else if (targetContainer && newContentContainer) {
                targetContainer.append(...newContentContainer.children);
            }

            this.offset += result.length;
        } else {
            const loadMoreButton = this.el.querySelector('.load-more-button');
            if (loadMoreButton) {
                loadMoreButton.style.display = 'none';
            }
        }
    };

    async _onLoadMoreClick(ev) {
        ev.preventDefault();
        await this.loadCategories();
    };
};

registry
    .category("public.interactions")
    .add("s_dynamic_sale_order_snippet.get_product_tab", SaleOrderSnippet);
registry
    .category("public.interactions.edit")
    .add("s_dynamic_sale_order_snippet.get_product_tab",
        {
            Interaction : SaleOrderSnippet
        });
