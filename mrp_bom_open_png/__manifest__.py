# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "MRP BOM Open PNG",
    "summary": "Adds path field to PNG drawing for Bill of Materials and its components.",
    "version": "13.0.0.0.0",
    "category": "Manufacture",
    "website": "None",
    'author': "Onduex sl",
    "license": "LGPL-3",
    "application": False,
    "depends": ["mrp", "rainbow", "insca3"],
    "data": [
        "views/some_view.xml",
        "views/report_mrpbomstructure.xml"
    ],
    "installable": True,
}
