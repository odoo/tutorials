import { _t } from "@web/core/l10n/translation";
import { patch } from '@web/core/utils/patch';
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { ProductScreen } from '@point_of_sale/app/screens/product_screen/product_screen';

patch(ProductScreen.prototype, {
    async addProductToOrder(product) {
        if (product.is_kit && (product.sub_product_ids && product.sub_product_ids.length != 0)) {
            this.dialog.add(ConfirmationDialog, {
                body: _t("You have to add sub-products ?"),
                confirm: async () => {    
                    for (let sub_product of product.sub_product_ids) {
                        await this.pos.addLineToCurrentOrder(
                            { product_id: sub_product },
                            {},
                            false
                        );
                    }
                },
                cancel: () => {},
            });
        }
        return await super.addProductToOrder(product);
    },
});
