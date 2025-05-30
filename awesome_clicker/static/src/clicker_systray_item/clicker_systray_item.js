import { registry } from "@web/core/registry";
import { Component, useState, useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";
    static props = {};

    document_click = 1;
    systray_button_click = 10;

    setup() {
        this.state = useState({ 
            counter: 0 
        });
        this.action = useService("action");
        this.listener = useExternalListener(document.body, "click", (e) => this.increment(e), { capture: true });
    }

    increment(event= null) {
        if (event.srcElement.id=="clicker_systray_button") { 
            this.state.counter +=this.systray_button_click;
        }
        else{
            this.state.counter += this.document_click;
        }
    }

    openClickerGame() { 
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name:"Clicker"
        })
    }
}

export const systrayItem = {
    Component: ClickerSystray,
};

registry.category("systray").add("awesome_clicker.ClickerSystray", systrayItem, { sequence: 1000 });
