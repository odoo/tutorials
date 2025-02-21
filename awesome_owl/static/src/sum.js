import { Counter } from "./counter";
import { Component, useState } from "@odoo/owl";

export class Sum extends Component{
     static template= "estate.Sum";
     static components= { Counter };
    
     setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
