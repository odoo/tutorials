import options from '@web_editor/js/editor/snippets.options';

function extractStyle(classString) {
    const regex = /(?:^|\s)o_(ribbon|tag)_(left|right)(?:\s|$)/;
    const matches = classString.match(regex);

    if (matches) {
        return {
            style: matches[1],
            position: matches[2]
        };
    } else {
        return {
            style: 'ribbon',
            position: 'left'
        };
    }
}


options.registry.WebsiteSaleProductsItem = options.registry.WebsiteSaleProductsItem.extend({
    willStart: async function () {
        const _super = this._super.bind(this);
        this.ribbonPositionClasses = {'left': 'o_ribbon_left o_tag_left', 'right': 'o_ribbon_right o_tag_right'};
        return _super(...arguments);
    },

    async setRibbonPosition(previewMode, widgetValue, params) {
        this._super(previewMode, widgetValue, params);
        const style = this.$ribbon[0].dataset?.style ?? extractStyle(this.$ribbon[0].className).style;
        this.$ribbon[0].className = this.$ribbon[0].className.replace(
            /o_(ribbon|tag)_(left|right)/, `o_${style}_${widgetValue}`
        );

        await this._saveRibbon();
    },

    async _computeWidgetState(methodName, params) {
        switch (methodName) {
            case 'setRibbonPosition': {
                return extractStyle(this.$ribbon[0].className).position;
            }
            case 'setRibbonStyle': {
                return this.$ribbon[0].dataset.style ||
                    extractStyle(this.$ribbon[0].className).style;
            }
        }
        return this._super(methodName, params);
    },

    async _saveRibbon(isNewRibbon = false) {
        this._super(isNewRibbon);
        const ribbonElement = this.$ribbon[0];
        const ribbon = {
            'name': this.$ribbon.text().trim(),
            'bg_color': ribbonElement.style.backgroundColor,
            'text_color': ribbonElement.style.color,
            'position': extractStyle(ribbonElement.className).position,
            'style': ribbonElement.dataset?.style ?? extractStyle(ribbonElement.className).style
        };
        ribbon.id = isNewRibbon ? Date.now() : parseInt(this.$target.closest('.oe_product')[0].dataset.ribbonId);
        this.trigger_up('set_ribbon', {ribbon});
        this.ribbons = await new Promise(resolve => this.trigger_up('get_ribbons', {callback: resolve}));
        this.rerender = true;
        await this._setRibbon(ribbon.id);
    },

    async _setRibbon(ribbonId) {
        this._super(ribbonId);
        const ribbon = (
            this.ribbons[ribbonId] ||
            {name: '', bg_color: '', text_color: '', position: 'left', style: 'ribbon'}
        );
        if (!ribbon.style) {
            ribbon.style = 'ribbon';
        }
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
