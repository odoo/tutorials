/** @odoo-module */

import {KeepLast} from "@web/core/utils/concurrency";

export class GalleryModel {
    constructor(orm, resModel, archInfo) {
        this.orm = orm;
        this.resModel = resModel;
        this.imageField = archInfo.imageField;
        this.limit = archInfo.limit;
        this.keeplast = new KeepLast();
    }

    async loadImages(domain) {
        const { records } = await this.keeplast.add(
            this.orm.webSearchRead(this.resModel, domain, {
                limit: this.limit,
                specification: {
                    [this.imageField]: {}
                },
                context: {
                    bin_size: true,
                }
            })
        );

        this.records = records;
    }
}
