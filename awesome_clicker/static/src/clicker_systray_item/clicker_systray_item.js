import { Component, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook";
import { ClickerValue } from "../clicker_value/clicker_value";

class ClickerSystrayItem extends Component {
    static template = "clicker_systray_item.ClickerSystrayItem";
    static components = { ClickerValue };

    setup() {
        super.setup();
        this.clicker = useClicker();
        useExternalListener(window, "click", this.clicker.increment, { capture: true });
    }
}
registry.category("systray").add("clicker_systray_item.ClickerSystrayItem", { Component: ClickerSystrayItem }, { sequence: 43 });
