/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { WysiwygAdapterComponent } from '@website/components/wysiwyg_adapter/wysiwyg_adapter';

patch(WysiwygAdapterComponent.prototype, {
    /**
     * @override
     */
    async init() {
        await super.init(...arguments);

        let ribbons = [];
        if (this._isProductListPage()) {
            ribbons = await this.orm.searchRead(
                'product.ribbon',
                [],
                ['id', 'name', 'bg_color', 'text_color', 'position', 'style']
            );
        }
        this.ribbons = Object.fromEntries(ribbons.map(ribbon => {
            return [ribbon.id, ribbon];
        }));
        this.originalRibbons = Object.assign({}, this.ribbons);
        this.productTemplatesRibbons = [];
        this.deletedRibbonClasses = '';
        this.ribbonPositionClasses = {'left': 'o_ribbon_left o_tag_left', 'right': 'o_ribbon_right o_tag_right'};
    }
});
