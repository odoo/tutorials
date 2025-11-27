import { registry } from "@web/core/registry";

export function getDashboardItems() {
    const itemsRegistry = registry.category("awesome_dashboard.items");
    const items = [];
    for (const entry of itemsRegistry.getEntries()) {
        items.push(entry[1]);
    }
    return items;
}
