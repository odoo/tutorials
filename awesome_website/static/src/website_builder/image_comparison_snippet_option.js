import { BaseOptionComponent } from "@html_builder/core/base_option_component";
import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";

export class ImageComparisonSnippetOption extends BaseOptionComponent {
    static template = "awesome_website.ImageComparisonSnippetOption";
    static selector = ".s_image_comparison";
}

export class ImageComparisonSnippetOptionPlugin extends Plugin {
    static id = "imageComparisonSnippetOption";
    resources = {
        builder_options: [ImageComparisonSnippetOption],
    };
}

registry
    .category("website-plugins")
    .add(ImageComparisonSnippetOptionPlugin.id, ImageComparisonSnippetOptionPlugin);
