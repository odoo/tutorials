// /** @odoo-module **/

// import publicWidget from "@web/legacy/js/public/public_widget";
// import { rpc } from "@web/core/network/rpc";

// publicWidget.registry.EstateDynamicSnippet = publicWidget.Widget.extend({

//     selector: '.s_property_cards',

//     start: function () {
//         this._loadProperties();
//         return this._super.apply(this, arguments);
//     },

//     _loadProperties: async function () {
//         const html = await rpc("/estate/get_property_data", {});
//         this.$el.html(html);
//     },

// });

/** @odoo-module */
import { DynamicSnippet } from "@website/snippets/s_dynamic_snippet/dynamic_snippet";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { markup } from "@odoo/owl";

export class EstateDynamicSnippet extends DynamicSnippet {
    static selector = ".s_property_cards"; // Matches your XML class

    async fetchData() {
        const nodeData = this.el.dataset;
        // We override fetchData to call your specific Real Estate controller
        const htmlContent = await rpc("/estate/get_property_data", {
            limit: nodeData.limit || 3,
            sort: nodeData.sort || 'name',
            category: nodeData.category || 'all',
        });
        // Odoo expects an array of marked-up strings
        this.data = [markup(htmlContent)]; 
    }

    renderContent() {
        // This puts the HTML into your .dynamic_snippet_template div
        const templateAreaEl = this.el.querySelector(".dynamic_snippet_template");
        templateAreaEl.innerHTML = this.data[0];
    }
}

// registry.category("public.interactions").add("estate.property_dynamic_snippet", EstateDynamicSnippet);
registry.category("public.interactions").add("EstateDynamicSnippet", EstateDynamicSnippet);


// import { BaseOptionComponent } from "@html_builder/core/utils";
// import { Plugin } from "@html_editor/plugin";
// import { registry } from "@web/core/registry";

// export class EstateSnippetOption extends BaseOptionComponent {
//     static template = "estate.EstateSnippetOption";
//     // This binds the sidebar options to your property cards snippet
//     static selector = ".s_property_cards"; 
// }

// export class EstateSnippetOptionPlugin extends Plugin {
//     static id = "estateSnippetOption";
//     resources = {
//         builder_options: [EstateSnippetOption],
//         // Adding the selector to inner content allows it to be dropped in other blocks
//         so_content_addition_selector: [".s_property_cards"],
//     };
// }

// registry.category("website-plugins").add(
//     EstateSnippetOptionPlugin.id,
//     EstateSnippetOptionPlugin
// );

/** @odoo-module */
// import options from '@web_editor/js/editor/snippets.options';
// import { rpc } from "@web/core/network/rpc";

// options.registry.EstatePropertySnippet = options.Class.extend({
//     // Trigger update whenever an attribute changes
//     async onUpdate() {
//         await this._fetchAndRender();
//     },

//     async _fetchAndRender() {
//         const data = this.$target.data();
        
//         // Call your controller via RPC
//         const html = await rpc('/estate/get_property_data', {
//             limit: data.limit || 3,
//             sort: data.sort || 'name',
//             category: data.category || 'all',
//         });

//         // Inject the rendered HTML into the template
//         this.$target.find('.dynamic_snippet_template').html(html || '<div class="alert alert-info">No properties found.</div>');
//     },
// });

/** @odoo-module */
// import options from 'web_editor.snippets.options';
// import { rpc } from "@web/core/network/rpc";

// options.registry.EstatePropertySnippet = options.Class.extend({
//     // This runs when the snippet is dropped or loaded
//     async start() {
//         await this._super(...arguments);
//         await this._fetchAndRender();
//     },

//     // This runs when you change options in the sidebar
//     async onUpdate() {
//         await this._fetchAndRender();
//     },

//     async _fetchAndRender() {
//         const data = this.$target.data();
        
//         // Fetch HTML from your controller
//         const html = await rpc('/estate/get_property_data', {
//             limit: data.limit || 3,
//             sort: data.sort || 'name',
//             category: data.category || 'all',
//         });

//         // Inject the returned HTML into the placeholder
//         this.$target.find('.dynamic_snippet_template').html(html);
//     },
// });