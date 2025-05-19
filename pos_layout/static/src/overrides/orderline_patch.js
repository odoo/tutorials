/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { xml } from "@odoo/owl";

patch(Orderline.prototype, {
    setup() {
        super.setup(...arguments);
    },
});

Orderline.props = {
    ...Orderline.props,
    isTableFormat: { type: Boolean, optional: true, default: false },
    isBoxedFormat: { type: Boolean, optional: true, default: false },
    lineIndex: { type: Number, optional: true },
};

Orderline.template = xml`
    <t t-if="props.isTableFormat">
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 5px;"><t t-esc="props.lineIndex + 1"/></td>
            <td style="padding: 5px;"><t t-esc="props.line.productName"/></td>
            <td style="text-align: center; padding: 5px;"><t t-esc="props.line.qty"/></td>
            <td style="text-align: center; padding: 5px;"><t t-esc="props.line.unitPrice"/></td>
            <td style="text-align: center; padding: 5px;"><t t-esc="props.line.price"/></td>
        </tr>
    </t>
    <t t-elif="props.isBoxedFormat">
        <!-- Box Format Orderline -->
        <tr>
            <td><t t-esc="props.lineIndex + 1"/></td>
            <td>
                <t t-esc="props.line.productName"/><br/>
                <span><t t-esc="props.line.qty"/> x <t t-esc="props.line.unitPrice"/></span><br/>
                <span t-if="props.line.hsn_code" class="hsn-code">HSN: <t t-esc="props.line.hsn_code"/></span>
            </td>
            <td><t t-esc="props.line.price"/></td>
        </tr>
    </t>
    <t t-else="">
        <t t-call="point_of_sale.Orderline"/>
    </t>
`;
