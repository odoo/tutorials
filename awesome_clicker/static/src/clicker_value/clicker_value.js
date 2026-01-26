import { Component } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers"

export class ClickerValue extends Component {
    static template = "awesome_clicker.ClientValue";

    static props = {
        value: Number
    }

    getValue() {
        return humanNumber(this.props.value)
    }
}
