/** @odoo-module **/

import {Component} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {Notebook} from "@web/core/notebook/notebook"
import {useClick} from "../../clicker/clicker";
import {ClickValue} from "../click_value/click_value";
import {ClickerBot} from "./clicker_bot/clicker_bot";

export class ClientAction extends Component {
    static template = "awesome_clicker.client_action";

    static components = {ClickValue, ClickerBot, Notebook}

    setup() {
        this.clicker = useClick()
    }

    buttonIncrement() {
        this.clicker.increment()
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
