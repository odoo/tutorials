import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const storageKey = "owl-dashboard-used-dashboard-items"

function setUsedItems(result, allItems, usedIds) {
    result.splice(0, result.length);

    for(let id of usedIds) {
        let found = allItems.find((i) => i.id == id);
        result.push(found);
    }
}

const dashboardItemsService = {
    start() {
        let fromStorage = localStorage.getItem(storageKey);
        let usedIds = fromStorage ? JSON.parse(fromStorage) : [];
        let allItems = registry.category("awesome_dashboard").get("items");
        let usedItems = reactive([]);

        setUsedItems(usedItems, allItems, usedIds);

        return {
            getUsedItems() {
                return usedItems;
            },
            getAllItems() {
                return allItems;
            },
            getUsedIds() {
                return usedIds.slice();
            },
            setUsedIds(ids) {
                usedIds = ids;
                localStorage.setItem(storageKey, JSON.stringify(ids));
                setUsedItems(usedItems, allItems, usedIds);
            }
        }
    }
}

registry.category("services").add("dashboard_items", dashboardItemsService);
