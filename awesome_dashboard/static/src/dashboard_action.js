
import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
console.log("1. dashboard_action.js loaded");


export class AwesomeDashboardLoader extends Component {
    static components = {
        LazyComponent,
    };
    
    static template = xml`
        <LazyComponent
            bundle="'awesome_dashboard.dashboard'"
            Component="'AwesomeDashboard'"
            />
    `;
}

console.log("2. Loader component defined");

registry.category("actions").add(
    "awesome_dashboard.dashboard",
    AwesomeDashboardLoader
);

console.log("3. Loader action registered");
// import { loadBundle } from "@web/core/assets";

// console.log("Loader file executed");

// loadBundle("awesome_dashboard.dashboard")
//     .then(() => {
//         console.log("Dashboard bundle loaded successfully");
//     })
//     .catch((error) => {
//         console.error("Dashboard bundle loading failed:", error);
//     });