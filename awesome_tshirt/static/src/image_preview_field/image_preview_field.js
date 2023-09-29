/** @odoo-module */

import { registry } from "@web/core/registry";
import { CharField } from "@web/views/fields/char/char_field";

const { Component } = owl;

class ImagePreviewField extends Component {}

ImagePreviewField.template = "awesome_tshirt.ImagePreviewField";
ImagePreviewField.components = { CharField };
ImagePreviewField.supportedTypes = ["char"];

registry.category("fields").add("image_preview", ImagePreviewField);