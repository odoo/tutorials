import { _t } from "@web/core/l10n/translation";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { NumberInputPopup } from "./number_input_popup";

patch(ControlButtons.prototype, {
    setup () {
        super.setup();
        this.action = useService("action");
    },

    async clickAddQuantity() {
        this.dialog.add(NumberInputPopup, {
            title: _t("Enter Quantity"),
            getPayload: (inputValue) => {
                return this.convertUom(inputValue);
            }
        });
    },
    convertUom(inputValue) {
        const order =  this.currentOrder;
        const line = order.get_selected_orderline();
        if (line) {
            const product = line.get_product();
            if (!product.second_uom_id){
                this.env.services.notification.add("Product Does not have Secondary Uom. Configure that first!", {
                      title: "Configuraion Issue!!",
                      type: "danger",
                      buttons: [
                          {
                              name: "Configure",
                              onClick: () => {
                                  this.action.doAction({
                                        type: 'ir.actions.act_window',
                                        name: _t('Product'),
                                        target: 'current',
                                        res_id: product.id,
                                        res_model: 'product.product',
                                        views: [[false, 'form']],
                                    });
                              },
                          },
                      ],
                });
                return false
            }
            const ratio = inputValue * (product.second_uom_id.factor_inv/product.uom_id.factor_inv);
            line.qty = parseFloat(ratio.toFixed(2));
            return true
        }
    },
    get currentOrder() {
        return this.pos.get_order();
    }
});
