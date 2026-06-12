/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

const CATEGORIES = [
    { value: "travel", label: "Travel" },
    { value: "food", label: "Food" },
    { value: "shopping", label: "Shopping" },
    { value: "other", label: "Other" },
];

export class ExpenseAction extends Component {
    static template = "expense_tracker.ExpenseAction";

    setup() {
        this.orm = useService("orm");
        this.categories = CATEGORIES;

        this.state = useState({
            showForm: false,
            expenses: [],
            form: {
                category: "other",
                price: "",
                description: "",
            },
        });

        onWillStart(async () => {
            await this.loadExpenses();
        });
    }

    async loadExpenses() {
        const result = await this.orm.searchRead(
            "tutorials.expense",
            [],
            ["id", "category", "price", "description"]
        );
        this.state.expenses = result;
    }

    showForm() {
        this.state.showForm = true;
    }

    onCategoryChange(ev) {
        this.state.form.category = ev.target.value;
    }

    onPriceChange(ev) {
        this.state.form.price = ev.target.value;
    }

    onDescriptionChange(ev) {
        this.state.form.description = ev.target.value;
    }

    async addExpense() {
        const price = parseFloat(this.state.form.price);

        if (!price || price <= 0) {
            return;
        }

        await this.orm.create("tutorials.expense", [
            {
                category: this.state.form.category,
                price: price,
                description: this.state.form.description,
            },
        ]);

        await this.loadExpenses();

        this.state.form = {
            category: "other",
            price: "",
            description: "",
        };
        this.state.showForm = false;
    }

    get totals() {
        const totals = {};

        for (const expense of this.state.expenses) {
            if (totals[expense.category]) {
                totals[expense.category] = totals[expense.category] + expense.price;
            } else {
                totals[expense.category] = expense.price;
            }
        }

        return totals;
    }

    displayCategory(categoryValue) {
        const found = this.categories.find(c => c.value === categoryValue);
        return found ? found.label : categoryValue;
    }
}

registry.category("actions").add("expense_tracker.expenses", ExpenseAction);
