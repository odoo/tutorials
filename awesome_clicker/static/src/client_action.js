
import { Component, useState } from "@odoo/owl";
import { Notebook } from "@web/core/notebook/notebook";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


export class AwesomeClickerClient extends Component {
    setup() {
        this.clicker = useState(useService("awesome_clicker_service"));
    }
    static components = { Notebook };
    static template = "awesome_clicker.client_action";
}

registry.category("actions").add("awesome_clicker.client_action", AwesomeClickerClient);
