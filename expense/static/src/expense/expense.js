import { browser } from '@web/core/browser/browser';
import { Component, useState } from "@odoo/owl";

export class Expense extends Component {
    static template = "expense.Expense";

    setup() {
        const savedExpenses = JSON.parse(browser.localStorage.getItem("expenses")) || []
        this.state = useState({
            description: "",
            amount: "",
            category: "Food",
            expenses: savedExpenses,
            filterCategory: "Food",
        });
    }

    addExpense() {
        this.state.expenses.push({
            id: this.state.expenses.length + 1,
            description:this.state.description,
            amount: Number(this.state.amount),
            category: this.state.category,
        });

        browser.localStorage.setItem("expenses",JSON.stringify(this.state.expenses));

        console.log(browser.localStorage.getItem("expenses"));

        this.state.description="";
        this.state.amount="";
        this.state.category="Food";
    }

    getCategoryTotal(category) {
        let total = 0;

        for (const expense of this.state.expenses) {
            if (expense.category === category) {
                total += expense.amount;
            }
        }

        return total;
    }

    getTotalExpense() {
        let total = 0;

        for (const expense of this.state.expenses) {
            total += expense.amount;
        }

        return total;
    }
}
