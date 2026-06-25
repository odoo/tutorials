import { Component} from "@odoo/owl";
import { Expense } from "./expense/expense";

export class Playground extends Component {
    static template = "expense.Playground";
    static components = { Expense };
}
