# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.rainbow.controllers.main import service_client, vault_log
from odoo.addons.rainbow.tools.tools import (
    convert_date,
    get_literal_by_records,
    SEARCH_OPERATORS,
    serialize_zeep_object_list,
    VAULT_SERVER_DATETIME_FORMAT,
)


class VaultServer(models.Model):
    _inherit = 'vault.server'
    _description = "Vault Server"

    @service_client(key="ITEM")
    @vault_log(action="Get products")
    def _list_vault_products(self, *args, **kw):
        self.ensure_one()
        search_conditions = self._prepare_search_conditions(
            request_type='import'
        )
        client = kw.get('client', False)
        bookmark = False
        items = []
        while bookmark is not None:
            params = dict(
                searchConditions=search_conditions,
                bRequestLatestOnly=True,
                bookmark=bookmark,
            )
            response = client.service.FindItemRevisionsBySearchConditions(
                **self._parse_request_params(params)
            )
            bookmark = response.bookmark
            result = response.FindItemRevisionsBySearchConditionsResult
            if result is not None:
                items += result.Item

        items = serialize_zeep_object_list(items)
        items = sorted(items, key=lambda r: r["MasterId"])

        return items
