import { useEffect } from "@odoo/owl";
import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";
import { formatCurrency } from "@point_of_sale/app/models/utils/currency";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { debounce } from "@web/core/utils/timing";

patch(OrderWidget.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.pos = usePos();
        
        this.validateOrderlines = debounce(this.validateOrderlines.bind(this), 1200);

        useEffect(() => {
            if (!this.props.lines || this.props.lines.length === 0) return;
            this.validateOrderlines();
        }, () => [() => this.props.lines]);
    },

    validateOrderlines() {
        const order = this.pos.get_order();
        if (!order || order.is_paid()) return;
        if (!this.props.lines) return;

        this.props.lines.forEach(lineProps => {
            const line = lineProps;
            const product = line.get_product();
            if (!product) return;

            const minPrice = product.min_price;
            const unitPrice = line.price_unit;
            const discountedUnitPrice = unitPrice * (1 - line.discount / 100);

            if ((unitPrice < minPrice) || (discountedUnitPrice < minPrice)) {
                this.dialog.add(AlertDialog, {
                    title: _t("Price Restriction"),
                    body: _t(
                        `You cannot sell ${product.display_name} below ${formatCurrency(minPrice, this.pos.currency)} (excluding taxes).`
                    ),
                });

                if (product.custom_price > 0) {
                    line.set_unit_price(product.custom_price);
                    line.price_type = "original";
                } else {
                    line.set_unit_price(product.lst_price);
                    line.price_type = "original";
                }

                if (line.discount > 0) {
                    line.set_discount(0);
                }
            }
        });
    },
});
