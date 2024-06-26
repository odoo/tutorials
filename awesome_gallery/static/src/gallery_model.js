/** @odoo-module **/

import { KeepLast } from "@web/core/utils/concurrency";

export class GalleryModel {
    constructor(orm, archInfo, resModel) {
        this.orm = orm;
        this.archInfo = archInfo;
        this.resModel = resModel;
        this.keepLast = new KeepLast();
        this.images = [];
    }

    async loadNewImages(domain) {
        this.images = await this.keepLast.add(this._loadImages(domain));
    }

    async _loadImages(domain) {
        const { _, records } = await this.orm.webSearchRead(this.resModel, domain, {
            specification: {
                [this.archInfo.image_field]: {},
            },
            context: {
                bin_size: true,
            },
        });
        return records;
    }
}
