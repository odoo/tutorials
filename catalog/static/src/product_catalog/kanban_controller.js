/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";
import { _t } from "@web/core/l10n/translation";

patch(ProductCatalogKanbanController.prototype, {
    /** override **/
    async _defineButtonContent() {
        if (this.orderResModel == 'catalog.catalog') {
            this.buttonString = _t("Back to Catalog")
        } else {
            super._defineButtonContent();
        }
    }
})
