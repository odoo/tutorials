/** @odoo-module */

import {KeepLast} from "@web/core/utils/concurrency";

export class GalleryModel {
    constructor(orm, resModel, archInfo, fields) {
        this.orm = orm;
        this.resModel = resModel;
        this.imageField = archInfo.imageField;
        this.pager = { limit: archInfo.limit, offset: 0 };
        this.fieldsForTooltip = archInfo.fieldsForTooltip;
        this.fields = fields;
        this.keeplast = new KeepLast();
    }

    async loadImages(domain) {

        const specification = {
            [this.imageField]: {},
            write_date: {},
        }

        for(const field of this.fieldsForTooltip) {
            specification[field] = {};
        }

        const { length, records } = await this.keeplast.add(
            this.orm.webSearchRead(this.resModel, domain, {
                limit: this.pager.limit,
                offset: this.pager.offset,
                specification,
                context: {
                    bin_size: true,
                }
            })
        );
        
        this.recordsLength = length;
        this.records = records;
    }

    async uploadImage(record_id, image, domain) {
        await this.orm.webSave(
            this.resModel,
            [record_id],
            {
                [this.imageField]: image,
            },
            {
                specification: {}
            }
        );

        await this.loadImages(domain);
    }
}
