import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";

    static props = {
        title: { type: String, optional: true },
        items: { type: Array, optional: true },
        close: Function,
        onApply: { type: Function, optional: true },
    };

    static components = { Dialog };

    setup() {
        this.orm = useService("orm");

        const allItems =
            this.props.items ||
            registry.category("awesome_dashboard.items").getAll();

        this.toHide = new Set();
        this.toShow = new Set();

        this.state = useState({
            items: allItems,
            removedItems: {},
        });

        onWillStart(async () => {
            const config = await this.orm.call(
                "res.users",
                "get_dashboard_config",
                [],
            );
            const hidden = config?.hidden_items || [];

            const removedMap = {};
            for (const id of hidden) {
                removedMap[String(id)] = true;
            }
            this.state.removedItems = removedMap;
        });
    }

    toggle = (item) => {
        const key = String(item.id);
        const isHidden = this.state.removedItems[key];

        if (isHidden) {
            delete this.state.removedItems[key];

            this.toShow.add(key);
            this.toHide.delete(key);
        } else {
            this.state.removedItems[key] = true;

            this.toHide.add(key);
            this.toShow.delete(key);
        }
    };

    isChecked(item) {
        return !this.state.removedItems[String(item.id)];
    }

    async apply() {
        const toHide = Array.from(this.toHide);
        const toShow = Array.from(this.toShow);

        if (toHide.length || toShow.length) {
            await this.orm.call("res.users", "update_dashboard_config", [
                toHide,
                toShow,
            ]);
        }

        if (this.props.onApply) {
            this.props.onApply();
        }

        this.props.close();
    }
}
