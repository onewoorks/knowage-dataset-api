from flask_restplus import Api

from .ep_contract import api as ep_contract_api
from .ep_supplier import api as ep_supplier_api
from .supplier_management import api as sm_performance_update_api
from .government_management import api as gm_performance_update_api

api = Api(
    title="CdcCms Knowage dataset API",
    version="1.0",
    description="An API for knowage dataset cockpit virtualization"
)

api.add_namespace(ep_contract_api)
api.add_namespace(ep_supplier_api)
api.add_namespace(sm_performance_update_api)
api.add_namespace(gm_performance_update_api)
