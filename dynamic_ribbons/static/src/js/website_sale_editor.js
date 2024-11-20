import options from "@web_editor/js/editor/snippets.options";

options.registry.WebsiteSaleProductsItem = options.registry.WebsiteSaleProductsItem.extend({    
    willStart: async function () {
        const _super = this._super.bind(this);
        this.ppr = this.$target.closest('[data-ppr]').data('ppr');
        this.defaultSort = this.$target[0].closest('[data-default-sort]').dataset.defaultSort
        this.productTemplateID = parseInt(this.$target.find('[data-oe-model="product.template"]').data('oe-id'));
        this.ribbonPositionClasses = {'left': 'o_ribbon_left o_tag_left', 'right': 'o_ribbon_right o_tag_right'};
        this.ribbons = await new Promise(resolve => this.trigger_up('get_ribbons', {callback: resolve}));
        this.$ribbon = this.$target.find('.o_ribbon');
        return _super(...arguments);
    },

    async setRibbonPosition(previewMode, widgetValue, params) {
        const ribbon = this.$ribbon[0];
        // Get the style (tag or ribbon) from the dataset or params
        const ribbonData = this.ribbons[this.$target[0].dataset.ribbonId] || {};
        const style = params?.style || ribbonData?.style || "ribbon";  // Safe access        // Remove both tag and ribbon position classes
        ribbon.classList.remove('o_ribbon_right', 'o_ribbon_left', 'o_tag_right', 'o_tag_left');
        
        // Add only the appropriate classes based on the selected style
        ribbon.classList.add(style === "ribbon" ? `o_ribbon_${widgetValue}` : `o_tag_${widgetValue}`);

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
                if (classList.contains('o_ribbon_left') || classList.contains('o_tag_left')) {
                    return 'left';
                }
                return 'right';
            }
            case 'setRibbonStyle': {
                return this.$ribbon.attr('data-style') ||
                    (this.$ribbon.hasClass('o_tag_left') || this.$ribbon.hasClass('o_tag_right') ? 'tag' : 'ribbon');
            }
        }
        return this._super(methodName, params);
    },

    async _saveRibbon(isNewRibbon = false) {
        const text = this.$ribbon.text().trim();

        const ribbon = {
            'name': text,
            'bg_color': this.$ribbon[0].style.backgroundColor,
            'text_color': this.$ribbon[0].style.color,
            'position': (this.$ribbon.attr('class').includes('o_ribbon_left') || this.$ribbon.attr('class').includes('o_tag_left')) ? 'left' : 'right',
            'style': this.$ribbon.attr('data-style') || 'ribbon',
        };
        ribbon.id = isNewRibbon ? Date.now() : parseInt(this.$target.closest('.oe_product')[0].dataset.ribbonId);
        this.trigger_up('set_ribbon', {ribbon: ribbon});
        this.ribbons = await new Promise(resolve => this.trigger_up('get_ribbons', {callback: resolve}));
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
            {name: '', bg_color: '', text_color: '', position: 'left', style: 'ribbon'}
        );
        // This option also manages other products' ribbon, therefore we need a
        // way to access all of them at once. With the content being in an iframe,
        // this is the simplest way.
        const $editableDocument = $(this.$target[0].ownerDocument.body);
        const $ribbons = $editableDocument.find(`[data-ribbon-id="${ribbonId}"] .o_ribbon`);
        $ribbons.empty().append(ribbon.name);
        $ribbons.removeClass('o_ribbon_left o_ribbon_right o_tag_left o_tag_right');

        const ribbonPositionClasses = ribbon.style === 'tag'
            ? (ribbon.position === 'left' ? 'o_tag_left' : 'o_tag_right')
            : (ribbon.position === 'left' ? 'o_ribbon_left' : 'o_ribbon_right');

        $ribbons.addClass(ribbonPositionClasses);
        $ribbons.attr('data-style', ribbon.style);
        $ribbons.css('background-color', ribbon.bg_color || '');
        $ribbons.css('color', ribbon.text_color || '');

        if (!this.ribbons[ribbonId]) {
            $editableDocument.find(`[data-ribbon-id="${ribbonId}"]`).each((index, product) => delete product.dataset.ribbonId);
        }

        // The ribbon does not have a savable parent, so we need to trigger the
        // saving process manually by flagging the ribbon as dirty.
        this.$ribbon.addClass('o_dirty');
    },

    async setRibbonStyle(previewMode, widgetValue, params) {
        this.$ribbon.attr('data-style', widgetValue);

        await this._saveRibbon();
    },
})
