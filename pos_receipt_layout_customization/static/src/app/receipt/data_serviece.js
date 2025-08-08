import { PosData } from "@point_of_sale/app/models/data_service";
import { patch } from "@web/core/utils/patch";
import { registerTemplate } from "@web/core/templates";


patch(PosData.prototype, {
    /**
     * @override
     */
    async loadInitialData(data) {
        const loadData = await super.loadInitialData(data);
        const qwebTemplatename = loadData["pos.session"]["data"][0]['template'].name
        const templateContent = loadData["pos.session"]["data"][0]['template'].template
    
        registerTemplate(qwebTemplatename, '', templateContent)
        return loadData;
    },
});
