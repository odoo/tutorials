import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook";


export class ClientAction extends Component {
    static template = "awesome_clicker.client_action";

    setup() {
        this.clicker = useClicker();
    }

    increment() {
        this.clicker.increment(9);
    }

}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
