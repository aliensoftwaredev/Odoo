=================================
Alien Software - Filter Selection
=================================
.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge2| image:: https://img.shields.io/badge/github-aliensoftwaredev%2FOdoo-lightgray.png?logo=github
    :target: https://github.com/aliensoftwaredev/Odoo
    :alt: aliensoftwaredev/Odoo

|badge1| |badge2|

Filter Selection

Usage
=====

You need to declare a selection field::

    ...
    name = fields.Char(string='Name')
    select = fields.Selection([('test1', 'Test 1'),
                               ('test2', 'Test 2'),
                               ('test3', 'Test 3'),
                               ('test4', 'Test 4')], string='Select')
    ...

In the view declaration, put widget='dynamic_selection' and alsw attribute in the field tag::

    ...
    <field name="select" widget="dynamic_selection" alsw="[{'domain': [('name', '=', False)], 'values': ['test1', 'test2']}, {'domain': [('name', '!=', False)], 'values': ['test3', 'test4']}]"/>
    ...

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/aliensoftwaredev/Odoo/issues>`_.
In case of trouble, please check there if your issue has already been reported.

Authors
~~~~~~~

* (Asian) Mai Tien Dung
* (America and EU) Dung Tien Mai

Maintainers
~~~~~~~~~~~

This module is maintained by the Alien Sofware.