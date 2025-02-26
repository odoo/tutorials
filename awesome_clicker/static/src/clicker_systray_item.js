import { registry } from "@web/core/registry";
import { Component, useState, useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "./clicker_hook";


class Clicker extends Component {
    static template = "awesome_clicker.clicker_systray_item";

    setup(){
        this.clicker = useClicker();
        useExternalListener(document.body, "click", () => this.clicker.increment(1), { capture: true });
        this.action = useService("action");
    }

    increment(){
        this.clicker.increment(9);
    }

    openClientAction(){
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker Game"
        });
    }

}

registry.category("systray").add("awesome_clicker.Clicker", { Component: Clicker });
