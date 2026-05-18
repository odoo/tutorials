FROM odoo:18.0

USER root

# system dependency for PDF reports
RUN apt-get update && apt-get install -y wkhtmltopdf

# create addons directory
RUN mkdir -p /mnt/extra-addons

# copy module (robust path handling)
COPY . /mnt/extra-addons/pharma_control_center

# copy start script
COPY start.sh /mnt/start.sh
RUN chmod +x /mnt/start.sh

# fix permissions
RUN chown -R odoo:odoo /mnt/extra-addons /mnt/start.sh

EXPOSE 8069

USER odoo

CMD ["/mnt/start.sh"]
