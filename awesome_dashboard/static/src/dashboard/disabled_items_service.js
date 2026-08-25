import { registry } from "@web/core/registry";
import { user } from "@web/core/user";

const disabledItemsService = {
    dependencies: ["orm"],

    start(env, { orm }) {
        return {
            async load() {
                const [data] = await orm.read("res.users", [user.userId], ["dashboard_disabled_items"]);
                return JSON.parse(data.dashboard_disabled_items || "[]");
            },
            save(ids) {
                return orm.write("res.users", [user.userId], {
                    dashboard_disabled_items: JSON.stringify(ids),
                });
            },
        };
    },
};

registry.category("services").add("awesome_dashboard.disabled_items", disabledItemsService);
