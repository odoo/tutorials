import options from "@web_editor/js/editor/snippets.options";


options.registry.WebsiteSaleProductsItem = options.registry.WebsiteSaleProductsItem.extend({

    async _computeWidgetState(methodName) {
        if (methodName === 'setRibbonStyle') {
            return this.$ribbon.attr('data-style') ||
                (this.$ribbon.hasClass('o_tag_left') || this.$ribbon.hasClass('o_tag_right') ? 'badge' : 'ribbon');
        }
        if (methodName === 'setRibbonPosition') {
            return this.$ribbon.hasClass('o_ribbon_left') || this.$ribbon.hasClass('o_tag_left') ? 'left' : 'right';
        }

        return this._super(...arguments);
    },

    async _saveRibbon(isNewRibbon = false) {
        const text = this.$ribbon.text().trim();

        const ribbon = {
            'name': text,
            'bg_color': this.$ribbon[0].style.backgroundColor,
            'text_color': this.$ribbon[0].style.color,
            'position': (this.$ribbon.attr('class').includes('o_ribbon_left') || this.$ribbon.attr('class').includes('o_tag_left')) ? 'left' : 'right',
            'style': this.$ribbon.attr('data-style'),
        };
        this.$ribbon.attr('data-style', ribbon.style);
        const ribbonId = isNewRibbon ? Date.now() : parseInt(this.$target.closest('.oe_product')[0].dataset.ribbonId);
        ribbon.id = ribbonId;
        this.$target[0].dataset.ribbonId = ribbonId;
        this.trigger_up('set_ribbon', { ribbon });
        this.ribbons = await new Promise(resolve => this.trigger_up('get_ribbons', { callback: resolve }));
        this.rerender = true;
        await this._setRibbon(ribbon.id);
    },

    async _setRibbon(ribbonId) {
        this.$target[0].dataset.ribbonId = ribbonId;
        this.trigger_up('set_product_ribbon', {
            templateId: this.productTemplateID,
            ribbonId: ribbonId || false,
        });
        const ribbon = (
            this.ribbons[ribbonId] ||
            { name: '', bg_color: '', text_color: '', position: 'left', style: 'ribbon' }
        );

        const $editableDocument = $(this.$target[0].ownerDocument.body);
        const $ribbons = $editableDocument.find(`[data-ribbon-id="${ribbonId}"] .o_ribbon, [data-ribbon-id="${ribbonId}"] .o_tag`);
        $ribbons.empty().append(ribbon.name);
        $ribbons.removeClass('o_ribbon_left o_ribbon_right o_tag_left o_tag_right');
        const positionClass = ribbon.style === 'badge'
            ? (ribbon.position === 'left' ? 'o_tag_left' : 'o_tag_right')
            : (ribbon.position === 'left' ? 'o_ribbon_left' : 'o_ribbon_right');

        $ribbons.addClass(positionClass);
        $ribbons.attr('data-style', ribbon.style);
        $ribbons.css('background-color', ribbon.bg_color || '');
        $ribbons.css('color', ribbon.text_color || '');

        if (!this.ribbons[ribbonId]) {
            $editableDocument.find(`[data-ribbon-id="${ribbonId}"]`).each((index, product) => delete product.dataset.ribbonId);
        }

        this.$ribbon.addClass('o_dirty');
    },

    async setRibbonStyle(previewMode, widgetValue, params) {
        this.$ribbon.attr('data-style', widgetValue);

        await this._saveRibbon();
    },

    async setRibbonPosition(previewMode, widgetValue, params) {
        const currentStyle = this.$ribbon.hasClass('o_tag_left') || this.$ribbon.hasClass('o_tag_right') ? 'badge' : 'ribbon';
        const positionClass = widgetValue === 'left'
            ? (currentStyle === 'badge' ? 'o_tag_left' : 'o_ribbon_left')
            : (currentStyle === 'badge' ? 'o_tag_right' : 'o_ribbon_right');

        this.$ribbon.removeClass('o_ribbon_left o_ribbon_right o_tag_left o_tag_right')
            .addClass(positionClass)
            .attr('data-style', currentStyle);

        await this._saveRibbon();
    },

});
