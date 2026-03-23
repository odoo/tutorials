import { DynamicSnippet } from "@website/snippets/s_dynamic_snippet/dynamic_snippet";
import { registry } from "@web/core/registry";
import { markup } from "@odoo/owl";
import { debounce } from "@web/core/utils/timing";

export class EstateDynamicSnippet extends DynamicSnippet {
    static selector = ".s_property_cards";

    setup() {
        super.setup();
        this._debouncedFetch = debounce(this._fetchAndRender.bind(this), 300);
    }

    start() {
        this._super(...arguments);
        this._fetchAndRender();
    }

    async fetchData() {
        const nodeData = this.el.dataset;

        try {
            const htmlContent = await this._rpc({
                route: "/estate/get_property_data",
                params: {
                    limit: nodeData.limit || 3,
                    sort: nodeData.sort || 'name',
                    category: nodeData.category || 'all',
                    show_price: nodeData.show_price || 'true',
                },
            });

            this.data = [markup(htmlContent)];
        } catch (error) {
            console.error('Error fetching property data:', error);
            // Fallback content when error occurs
            this.data = [markup(`
                <div class="col-12">
                    <div class="alert alert-danger" role="alert">
                        <i class="fa fa-exclamation-triangle me-2"></i>
                        Unable to load properties. Please try again later.
                    </div>
                </div>
            `)];
        }
    }

    renderContent() {
        const el = this.el.querySelector(".dynamic_snippet_template");
        if (el && this.data && this.data[0]) {
            el.innerHTML = this.data[0];
        }
    }

    onWillUpdateProps() {
        this._debouncedFetch();
    }

    async _fetchAndRender() {
        try {
            await this.fetchData();
            this.renderContent();
        } catch (error) {
            console.error('Error in fetch and render:', error);
        }
    }
}

registry.category("public.interactions").add("EstateDynamicSnippet", EstateDynamicSnippet);

// import { DynamicSnippet } from "@website/snippets/s_dynamic_snippet/dynamic_snippet";
// import { registry } from "@web/core/registry";
// import { rpc } from "@web/core/network/rpc";
// import { markup } from "@odoo/owl";

// export class EstateDynamicSnippet extends DynamicSnippet {
//     static selector = ".s_property_cards"; // Matches your XML class

//     async fetchData() {
//         const nodeData = this.el.dataset;
//         // We override fetchData to call your specific Real Estate controller
//         const htmlContent = await rpc("/estate/get_property_data", {
//             limit: nodeData.limit || 3,
//             sort: nodeData.sort || 'name',
//             category: nodeData.category || 'all',
//         });
//         // Odoo expects an array of marked-up strings
//         this.data = [markup(htmlContent)]; 
//     }

//     renderContent() {
//         // This puts the HTML into your .dynamic_snippet_template div
//         const templateAreaEl = this.el.querySelector(".dynamic_snippet_template");
//         templateAreaEl.innerHTML = this.data[0];
//     }
// }

// registry.category("public.interactions").add("EstateDynamicSnippet", EstateDynamicSnippet);
