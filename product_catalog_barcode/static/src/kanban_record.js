/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { useService, useBus } from "@web/core/utils/hooks";
import { addScannedProduct } from "./scanned_products";
import { onMounted } from "@odoo/owl";


patch(ProductCatalogKanbanRecord.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.barcodeService = useService("barcode");
        this.notification = useService("notification");
        this._barcodeHandler = (ev) => {
            this._onBarcodeScanned(ev.detail.barcode);
        };
        useBus(this.barcodeService.bus, "barcode_scanned", this._barcodeHandler);
        onMounted(() => {
            document.activeElement.blur();
        });
    },
    async _onBarcodeScanned(barcode) {
        if (!barcode) return;
        const [product] = await this.orm.searchRead(
            "product.product",
            [['barcode', '=', barcode]],
            ['id', 'display_name'],
            { limit: 1 }
        );
        if (!product) {
            this.notification.add("Product not found", { type: 'warning' });
            return;
        }
        const isVisible = this._isProductVisible(product.id);
        addScannedProduct(product.id);

        if (isVisible) {
            if (this.props.record.resId === product.id) {
                if (this.props.record.productCatalogData.quantity > 0) {
                    this.increaseQuantity();
                    this.notification.add(
                        "Increased quantity",
                        { type: 'success' }
                    );
                } else {
                    this.addProduct();
                    this.notification.add(
                        "Added product",
                        { type: 'success' }
                    );
                }
            }
        }
        else {
            await this._loadAndFocusProduct(product.id);
        }
    },

    _isProductVisible(productId) {
        return this.props.list.records.some(record => record.resId === productId);
    },

    async _loadAndFocusProduct(productId) {
        await this.props.list.model.load({
            domain: [['id', '=', productId]],
            limit: 1
        });
    }
});
