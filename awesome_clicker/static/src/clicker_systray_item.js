import { Component, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "./clicker_hook";
import { useService } from "@web/core/utils/hooks";
import { ClickValue } from "./clicker_value";

class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";
    static components = { ClickValue: ClickValue };

    setup() {
        this.action = useService("action");
        this.clicker = useClicker();
        this.onClick = this.onClick.bind(this); // bind the method to the instance to have the correct event.target
        useExternalListener(document.body, "click", (event) => {
            this.clicker.increment(1)
        }, { capture: true });
        this.state = this.clicker.state;
    }

    onClick(event) {
        // this.clicker.increment(1);
        // event.stopPropagation();
    }

    openAction() {
        console.log("open action");
        this.action.doAction("awesome_clicker.action_awesome_clicker_client_action");
        // this.action.doAction({
        //     type: "ir.actions.client",
        //     tag: "awesome_clicker.client_action",
        //     name: "Awesome Clicker",
        //     target: "new",
        // });

    }
}

registry.category("systray").add("clicker_systray_item", { Component: ClickerSystrayItem }, { sequence: 100 });
