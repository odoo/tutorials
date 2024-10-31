/** @odoo-module **/

import {Component} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {useClick} from "../../clicker/clicker";
import {ClickValue} from "../click_value/click_value";

export class SystrayItem extends Component {
    static template = "awesome_clicker.systray_item";

    static components = {ClickValue}


    setup() {
        this.clicker = this.clicker = useClick()
        this.action = useService("action")
    }

    increment() {
        this.clicker.increment()
    }

    buttonIncrement() {
        this.clicker.increment()
    }

    openClicker() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        })
    }
}

registry.category("systray").add("awesome_clicker.systray_item", {
    Component: SystrayItem,
});
