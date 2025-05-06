import options from '@web_editor/js/editor/snippets.options';

options.registry.WebsiteSaleProductsItem = options.registry.WebsiteSaleProductsItem.extend({
    willStart: async function () {
        const _super = this._super.bind(this);
        this.ppr = this.$target.closest('[data-ppr]').data('ppr');
        this.defaultSort = this.$target[0].closest('[data-default-sort]').dataset.defaultSort;
        this.productTemplateID = parseInt(this.$target.find('[data-oe-model="product.template"]').data('oe-id'));
        this.ribbonPositionClasses = {'left': 'o_ribbon_left o_tag_left', 'right': 'o_ribbon_right o_tag_right'};
        this.ribbons = await new Promise(resolve => this.trigger_up('get_ribbons', {callback: resolve}));
        this.$ribbon = this.$target.find('.o_ribbon');
        return _super(...arguments);
    },

    async setRibbonPosition(previewMode, widgetValue, params) {
        const ribbonClasses = this.$ribbon[0].classList;
        const ribbonData = this.ribbons[this.$target[0].dataset.ribbonId] || {};
        const style = params?.style || ribbonData?.style || 'ribbon';
        ribbonClasses.remove('o_ribbon_right', 'o_ribbon_left', 'o_tag_right', 'o_tag_left');
        ribbonClasses.add(`o_${style}_${widgetValue}`);

        await this._saveRibbon();
    },

    async _computeWidgetState(methodName, params) {
        const classList = this.$ribbon[0].classList;
        switch (methodName) {
            case 'setRibbon':
                return this.$target.attr('data-ribbon-id') || '';
            case 'setRibbonName':
                return this.$ribbon.text();
            case 'setRibbonPosition': {
                return (
                    classList.contains('o_ribbon_left')
                    || classList.contains('o_tag_left')
                ) ? 'left' : 'right';
            }
            case 'setRibbonStyle': {
                return this.$ribbon.attr('data-style') ||
                    ((
                        classList.contains('o_tag_left')
                        || classList.contains('o_tag_right')
                    ) ? 'tag' : 'ribbon');
            }
        }
        return this._super(methodName, params);
    },

    async _saveRibbon(isNewRibbon = false) {
        const ribbonElement = this.$ribbon[0];
        const ribbon = {
            'name': this.$ribbon.text().trim(),
            'bg_color': ribbonElement.style.backgroundColor,
            'text_color': ribbonElement.style.color,
            'position': (ribbonElement.classList.contains('o_ribbon_left') || ribbonElement.classList.contains('o_tag_left')) ? 'left' : 'right',
            'style': ribbonElement.dataset?.style || 'ribbon'
        };
        ribbon.id = isNewRibbon ? Date.now() : parseInt(this.$target.closest('.oe_product')[0].dataset.ribbonId);
        this.trigger_up('set_ribbon', {ribbon});
        this.ribbons = await new Promise(resolve => this.trigger_up('get_ribbons', {callback: resolve}));
        this.rerender = true;
        await this._setRibbon(ribbon.id);
    },

    async _setRibbon(ribbonId) {
        this.$target[0].dataset.ribbonId = ribbonId;
        this.trigger_up('set_product_ribbon', {
            templateId: this.productTemplateID,
            ribbonId: ribbonId || false
        });
        const ribbon = (
            this.ribbons[ribbonId] ||
            {name: '', bg_color: '', text_color: '', position: 'left', style: 'ribbon'}
        );

        const $editableDocument = $(this.$target[0].ownerDocument.body);
        const $ribbons = $editableDocument.find(`[data-ribbon-id="${ribbonId}"] .o_ribbon`);
        $ribbons.empty().append(ribbon.name);
        $ribbons.removeClass('o_ribbon_left o_tag_left o_ribbon_right o_tag_right');

        $ribbons.addClass(`o_${ribbon.style}_${ribbon.position}`);
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
    }
});
