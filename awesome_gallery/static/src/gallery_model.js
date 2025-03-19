import { xml } from '@odoo/owl';
import { KeepLast } from '@web/core/utils/concurrency';
import { createElement } from '@web/core/utils/xml';

export class GalleryModel {
    constructor(model, orm, archInfo) {
        this.keepLast = new KeepLast();
        this.orm = orm;
        this.model = model;
        this.imageField = archInfo.imageField;
        this.tooltipFields = archInfo.tooltipFields;
        this.records = [];
        this.offset = 0;
        this.limit = 10;
        this.total = 0;
        const fieldElements = archInfo.tooltipTemplate.querySelectorAll('field');
        for (const fieldElement of fieldElements) {
            const fieldName = fieldElement.getAttribute('name');
            fieldElement.insertAdjacentHTML('afterend', `<t t-out="record['${fieldName}']" />`);
            fieldElement.remove();
        }
        const tooltip = createElement('t', [...archInfo.tooltipTemplate.children]).outerHTML;
        this.tooltipTemplate = xml`${tooltip}`;
    }

    async load(domain) {
        const specification = {
            [this.imageField]: {},
            ['write_date']: {}
        };
        for (const field of this.tooltipFields) {
            specification[[field]] = {};
        }
        const { length, records } = await this.keepLast.add(this.orm.webSearchRead(this.model, domain, {
            specification,
            context: {
                bin_size: true,
            },
            offset: this.offset,
            limit: this.limit,
        }));
        this.records = records;
        this.total = length;
    }

    async uploadImage(id, data, domain) {
        await this.orm.webSave(
            this.model,
            [id],
            {
                [this.imageField]: data
            },
            {
                specification: {}
            }
        );
        await this.load(domain);
    }
}
