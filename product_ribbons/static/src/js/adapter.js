import { WysiwygAdapterComponent } from '@website/components/wysiwyg_adapter/wysiwyg_adapter';
import { patch } from "@web/core/utils/patch";


patch(WysiwygAdapterComponent.prototype, {

    async init() {
        await super.init(...arguments);

        let ribbons = [];
        if (this._isProductListPage()) {
            ribbons = await this.orm.searchRead(
                'product.ribbon',
                [],
                ['id', 'name', 'bg_color', 'text_color', 'position', 'style'],
            );
        }
        this.ribbons = Object.fromEntries(ribbons.map(ribbon => [ribbon.id, ribbon]));
        this.originalRibbons = Object.assign({}, this.ribbons);
        this.productTemplatesRibbons = [];
        this.deletedRibbonClasses = '';
        this.stylePositionClasses = {
            'ribbon': { 'left': 'o_ribbon_left', 'right': 'o_ribbon_right' },
            'badge': { 'left': 'o_tag_left', 'right': 'o_tag_right' },
        };
    },

    _onGetRibbonClasses(ev) {
        const classes = Object.values(this.ribbons).reduce((classes, ribbon) => {
            const style = ribbon.style || 'ribbon';
            return classes + ` ${this.stylePositionClasses[style][ribbon.position]}`;
        }, '') + this.deletedRibbonClasses;
        ev.data.callback(classes);
    },

    _onDeleteRibbon(ev) {
        const ribbon = this.ribbons[ev.data.id];
        const style = ribbon.style || 'ribbon';
        this.deletedRibbonClasses += ` ${this.stylePositionClasses[style][ribbon.position]}`;
        delete this.ribbons[ev.data.id];
    },

    _onSetRibbon(ev) {
        const { ribbon } = ev.data;
        const previousRibbon = this.ribbons[ribbon.id];
        if (previousRibbon) {
            const prevStyle = previousRibbon.style || 'ribbon';
            this.deletedRibbonClasses += ` ${this.stylePositionClasses[prevStyle][previousRibbon.position]}`;
        }
        this.ribbons[ribbon.id] = ribbon;
    },
});
