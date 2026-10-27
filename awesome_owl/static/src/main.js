import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";
import { TodoApp } from "./todo_list";

const config = {
    dev: true,
    name: "Owl Tutorial"
};

const isTodoPage = window.location.pathname === "/awesome_owl/todo"
    || new URLSearchParams(window.location.search).get("page") === "todo";

// Odoo's mountComponent JSDoc types this as an instance, but it expects a component class.
/** @type {any} */
const RootComponent = isTodoPage ? TodoApp : Playground;

whenReady(() => mountComponent(RootComponent, document.body, config));
