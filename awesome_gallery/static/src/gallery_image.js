import { Component, useState } from '@odoo/owl';
import { FileUploader } from '@web/views/fields/file_handler';
import { url } from '@web/core/utils/urls';
import { useService } from '@web/core/utils/hooks';
import { useTooltip } from '@web/core/tooltip/tooltip_hook';

export class GalleryImage extends Component {
    static template = 'awesome_gallery.GalleryImage';
    static components = { FileUploader };
    static props = {
        model: Object,
        record: Object,
        onImageUpload: Function
    };

    setup() {
        this.hasImage = Boolean(this.props.model.imageField);
        this.orm = useService('orm');
        this.action = useService('action');
        this.state = useState({
            url: this._getURL()
        });

        useTooltip('tooltip', {
            info: { record: this.props.record },
            template: this.props.model.tooltipTemplate,
        });
    }

    _getURL() {
        return url('/web/image', {
            model: this.props.model.model,
            id: this.props.record.id,
            field: this.props.model.imageField,
            write_date: this.props.record.write_date
        });
    }

    showForm() {
        this.action.switchView('form', { resId: this.props.record.id });
    }

    async uploadImage(img) {
        await this.props.onImageUpload(this.props.record.id, img.data);
        this.state.url = this._getURL();
    }
};
