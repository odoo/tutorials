import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { ExpenseCard } from "./expense_tracker/expense_tracker";

const config = {
    dev: true,
    name: "Expence Tracker" 
};

// Mount the Playground component when the document.body is ready
whenReady(() => mountComponent(ExpenseCard, document.body, config));
