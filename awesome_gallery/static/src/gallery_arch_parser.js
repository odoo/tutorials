import { visitXML } from '@web/core/utils/xml';

export class GalleryArchParser {
    parse(arch) {
        const imageField = arch.getAttribute('image_field');
        const tooltipFields = [];
        let tooltipTemplate = null;
        visitXML(arch, node => {
            switch (node.tagName) {
                case 'tooltip-template': {
                    tooltipTemplate = node;
                    break;
                }
                case 'field': {
                    tooltipFields.push(node.getAttribute('name'));
                    break;
                }
            }
        });
        return {
            imageField,
            tooltipFields,
            tooltipTemplate,
        }
    }
};
