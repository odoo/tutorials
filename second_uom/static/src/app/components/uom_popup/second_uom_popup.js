import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";

export class SecondUomPopup extends NumberPopup {
    static template = "second_uom.SecondUomPopup";
    static props = {
        ...NumberPopup.props,
        uomName: { type: String },
    };

    confirm() {
    this.props.getPayload(this.state.buffer);
    this.props.close();
    }
}
