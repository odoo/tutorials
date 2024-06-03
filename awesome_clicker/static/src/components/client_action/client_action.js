/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClickerService } from "../../core/hooks";

export class ClientAction extends Component {
    static template = "awesome_clicker.client_action";

    setup() {
        this.clickerService = useClickerService();
    }

    onButtonClick() {
        this.clickerService.increment(10);
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
