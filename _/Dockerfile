FROM odoo:17

USER root
RUN pip3 install --upgrade pip
# Install pydevd_pycharm
RUN pip3 install pydevd-pycharm~=241.17890.14
# Optional: Install pydevd-odoo
RUN pip3 install pydevd-odoo
# Add Port for debugging
ENV ODOO_DEBUG_PORT=8889
# Add pydevd_pycharm to odoo/__init__.py
RUN echo "try:" >> /usr/lib/python3/dist-packages/odoo/__init__.py \
    && echo "    import pydevd_pycharm" >> /usr/lib/python3/dist-packages/odoo/__init__.py \
    && echo "    pydevd_pycharm.settrace('host.docker.internal', port=$ODOO_DEBUG_PORT, stdoutToServer=True, stderrToServer=True, suspend=False)" >> /usr/lib/python3/dist-packages/odoo/__init__.py \
    && echo "except Exception as e:" >> /usr/lib/python3/dist-packages/odoo/__init__.py \
    && echo "    print('An error occurred:', e)" >> /usr/lib/python3/dist-packages/odoo/__init__.py



USER odoo