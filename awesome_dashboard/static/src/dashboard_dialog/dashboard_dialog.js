import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardDialog extends Component {
    static template = "awesome_dashboard.DashboardDialog";
    static props = {
        close: Function,
        items: {
            type: Object,
        },
        itemsState: {
            type: Object,
        }
    }
    static components = { Dialog }
    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.orm = useService("orm");
        this.state = useState({ saving: false });
    }

    async _confirm() {
        this.state.saving = true;
        const checkboxes = document.getElementsByClassName("form-check-input");
        const settings = Array.from(checkboxes).reduce((acc, checkbox) => {
            const id = 'dataset' in checkbox ? checkbox.dataset['id'] : null;
            const visibility = 'checked' in checkbox ? checkbox.checked : false;
            acc = { ...acc, [id]: visibility }
            return acc;
        }, {});
        await this.setConfigSetting(settings);
        location.reload();
        this.props.close();
        this.state.saving = false;
    }

    async setConfigSetting(data) {
        const value = await this.orm.call("res.config.settings", "web_save",
            [[], [data]],
            { context: { model: 'awesome_dashboard' }, specification: {} })

        const res = await this.orm.call("res.config.settings", "execute", [[value[0].id]], { context: { model: 'awesome_dashboard' } });
        return value;
    }
}
