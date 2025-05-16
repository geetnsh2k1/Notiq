from models.template import Template
from schema.template import TemplateCreate, TemplateDetails

class TemplateMapper:
    @staticmethod
    def template_create_to_model(template_create: TemplateCreate) -> Template:
        """
        Converts a TemplateCreate DTO to a Template model instance.

        Args:
            template_create (TemplateCreate): The DTO containing template creation data.

        Returns:
            Template: The Template model instance.
        """
        return Template(
            channel_id=template_create.channel_id,
            provider_id=template_create.provider_id,
            template_ref_id=template_create.template_ref_id,
            template_name=template_create.template_name,
            description=template_create.description,
            meta_data=template_create.meta_data,
            schema=template_create.schema,
        )

    @staticmethod
    def model_to_template_response(template: Template) -> TemplateDetails:
        """
        Converts a Template model instance to a TemplateDetails DTO.

        Args:
            template (Template): The Template model instance.

        Returns:
            TemplateDetails: The DTO containing template details.
        """
        return TemplateDetails(
            id=template.id,
            channel_id=template.channel_id,
            provider_id=template.provider_id,
            template_ref_id=template.template_ref_id,
            template_name=template.template_name,
            description=template.description,
            meta_data=template.meta_data,
            schema=template.schema,
        )