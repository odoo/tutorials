import { Component } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";
import { useClicker } from "../clicker_hook";


export class ClickValue extends Component {
    static template = "awesome_clicker.click_value";

    setup() {
        this.clicker = useClicker();
    }

    get clicks(){
        return humanNumber(this.clicker.clicks, { decimals: 1 });
    }
}
