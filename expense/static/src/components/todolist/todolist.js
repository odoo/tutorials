import { Component, useState, useRef, useEffect, onMounted } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";

    static components = {
        TodoItem,
    };

    static props = {};

    setup() {
        this.nextId = 1;
        this.state = useState({
            todos: [],
            category: "",
            sumFor1stCategory: 0,
            sumFor2stCategory: 0,
            sumFor3stCategory: 0,
            filteredExpenses: [],
            TotalExpense: 0,
        });

        this.nameRef = useRef("nameInput");
        this.amountRef = useRef("amountInput")
        this.categoryInput = useRef("categoryInput")

        useEffect(() => {
            this.totalAmount(),
                () => [this.state.todos]
        })

        useEffect(() => {
            this.filterExpenses(),
                () => [this.state.filteredExpenses]
        })

        onMounted(() => {
            this.nameRef.el.focus();
        });
    }

    todoCount() {
        this.nextId = this.state.todos.length + 1;
    }

    handleDelete(id) {
        const index = this.state.todos.findIndex((todo) => todo.id === id);
        this.state.todos.splice(index, 1);
        this.state.todos.forEach((todo, index) => {
            todo.id = index + 1;
        });
        this.todoCount()
    }

    toggleState(id) {
        this.state.todos.find(t => t.id === id) ? todo.isCompleted = !todo.isCompleted : ""
    }

    clearAll() {
        this.state.todos = []
    }

    markAll() {
        this.state.todos.filter(t => t.isCompleted == false).forEach((todo) => {
            todo.isCompleted = true
        });
    }

    filterExpenses() {

        this.state.filteredExpenses = this.state.todos.filter(t => t.category === this.state.category)
    }
    totalAmount() {
        const categories = ["Food", "More Food", "Even More Food"]
        categories.forEach((category) => {

            let filterByCategoty = this.state.todos.filter(t => t.category == category)
            let sum = 0

            for (var i = 0; i < filterByCategoty.length; i++) {

                sum = sum + filterByCategoty[i].amount
            }
            if (category === "Food") {
                this.state.sumFor1stCategory = sum
            }
            else if (category === "More Food") {
                this.state.sumFor2stCategory = sum
            }
            else if (category === "Even More Food") {
                this.state.sumFor3stCategory = sum
            }
            this.state.TotalExpense = this.state.sumFor3stCategory + this.state.sumFor2stCategory + this.state.sumFor1stCategory
        });

    }

    addTodo(ev) {



        this.nameRef.el.value === "" || this.amountRef.el.value === "" ?
            alert("Feel Something") :
            console.log("this.amountRef.el.value----------", this.amountRef.el.value.typeOf)
        this.state.todos.push({
            id: this.nextId++,
            title: this.nameRef.el.value.trim(),
            isCompleted: false,
            amount: parseFloat(this.amountRef.el.value),
            category: this.state.category,
        });

        // if (ev.key === "Enter" && ev.target.value.trim() !== "") {
        //     this.state.todos.find(t => t.title === ev.target.value.trim()) ? alert("Cant write a duplicate todo")
        //         : this.state.todos.push({
        //             id: this.nextId++,
        //             title: ev.target.value.trim(),
        //             isCompleted: false,
        //             amount: ev.target.value.trim(),
        //         });
        //     ev.target.value = "";
        // }
    }

}