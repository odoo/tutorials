import { Component } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";
import { useClicker } from "./useClicker";

export class ClickerValue extends Component {
    static template = "awesome_clicker.ClickerValue";
    static props = {};

    setup() {
        this.clicker = useClicker();
    }

    get humanizedClicks() {
        return humanNumber(this.clicker.state.clicks, {
            decimals: 1,
        });
    }
}