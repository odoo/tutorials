/** @odoo-module **/

import publicWidget from "@web_editor/js/public/widget";

publicWidget.registry.dynamic_snippet_sale_order = publicWidget.Widget.extend({
    selector: ".categories_section",

    xmlDependencies: ["/website_dynamic_snippet/static/src/xml/sale_order_snippet.xml"],

    start: function () {
        this.layout = this.el.dataset.layout || 'list';
        this._render();
        return this._super(...arguments);
    },

    _render: function () {
        this._rpc({
            route: '/your/data/route',
            params: { /* your logic */ },
        }).then(data => {
            this.$el.find(".card_list_wrapper").html(
                qweb.render("website_dynamic_snippet.sale_order_snippet", {
                    result: data.orders,
                    layout: this.layout,
                })
            );
        });
    },

    onChangeOption(previewMode, widgetValue, params) {
        if (['grid', 'list'].includes(widgetValue)) {
            this.layout = widgetValue;
            this._render();
        }
    },
});
