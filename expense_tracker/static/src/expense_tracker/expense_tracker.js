import { Component, useState } from "@odoo/owl";

export class ExpenseCard extends Component {
    static template = "expense_tracker.ExpenseCard";

    setup() {
        this.state = useState({
            isOpen: false,
            description: "",
            amount: "",
            category: "",
            expenses: [],
        });
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }

    onDescriptionInput(ev) {
        this.state.description = ev.target.value;
    }

    onAmountInput(ev) {
        this.state.amount = ev.target.value;
    }

    onCategoryChange(ev) {
        this.state.category = ev.target.value;
    }

    saveExpense() {
        const { description, amount, category } = this.state;
        if (!description || !amount || !category) return;

        this.state.expenses.push({
            description,
            amount: parseFloat(amount),
            category,
        });

        this.state.description = "";
        this.state.amount = "";
        this.state.category = "";

        this.toggleContent();
    }

    get foodTotal() {
        return this.state.expenses.filter(e => e.category === "Food")
            .reduce((sum, e) => sum + e.amount, 0);
    }

    get travelTotal() {
        return this.state.expenses.filter(e => e.category === "Travel")
            .reduce((sum, e) => sum + e.amount, 0);
    }

    get shoppingTotal() {
        return this.state.expenses.filter(e => e.category === "Shopping")
            .reduce((sum, e) => sum + e.amount, 0);
    }

    get otherTotal() {
        return this.state.expenses.filter(e => e.category === "Other")
            .reduce((sum, e) => sum + e.amount, 0);
    }

    get grandTotal() {
        return this.state.expenses.reduce((sum, e) => sum + e.amount, 0);
    }
}
