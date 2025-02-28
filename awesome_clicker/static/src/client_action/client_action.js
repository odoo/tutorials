import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook";
import { humanNumber } from "@web/core/utils/numbers";
import { ClickValue } from "../click_value/click_value";


export class ClientAction extends Component {
    static template = "awesome_clicker.client_action";
    static components = { ClickValue };

    setup() {
        this.clicker = useClicker();
    }

}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
