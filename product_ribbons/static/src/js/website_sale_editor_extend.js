import options from "@web_editor/js/editor/snippets.options";


options.registry.WebsiteSaleProductsItem = options.registry.WebsiteSaleProductsItem.extend({

    async setRibbonStyle(previewMode, widgetValue, params) {
        this.$ribbon.attr('data-style', widgetValue);

        if (!previewMode) {
            await this._saveRibbon();
        }
    },

    async _saveRibbon(isNewRibbon = false) {
        const text = this.$ribbon.text().trim();
        const ribbon = {
            'name': text,
            'bg_color': this.$ribbon[0].style.backgroundColor,
            'text_color': this.$ribbon[0].style.color,
            'position': (this.$ribbon.attr('class').includes('o_ribbon_left')) ? 'left' : 'right',
            'style': this.$ribbon.attr('data-style') || 'ribbon',
        };
        ribbon.id = isNewRibbon ? Date.now() : parseInt(this.$target.closest('.oe_product')[0].dataset.ribbonId);
        this.trigger_up('set_ribbon', {ribbon: ribbon});
        this.ribbons = await new Promise(resolve => this.trigger_up('get_ribbons', {callback: resolve}));
    },

    async _computeWidgetState(methodName, params) {
        if (methodName === 'setRibbonStyle') {
            return this.$ribbon.attr('data-style') || 'ribbon';
        }
        return this._super(methodName, params);
    },

});