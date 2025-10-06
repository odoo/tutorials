import { Component } from "@odoo/owl";
import { useClicker } from "../clicker_hook";

export class ClickBots extends Component {
    static template = "awesome_clicker.ClickBots";
    static props = {};

    setup() {
        this.clicker = useClicker();
    }

}
