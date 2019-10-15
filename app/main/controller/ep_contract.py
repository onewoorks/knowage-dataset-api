from flask_restplus import Namespace, Resource, fields
from ..model.ep_contract import EpContract

api = Namespace('ep_contract',description="EP Contract records")
ep_contract = EpContract()

@api.route('/')
class EPContractList(Resource):
    @api.doc('list ep contract')
    def get(self):       
        response = ep_contract.get_all_contract()
        return {
            'result':response
        }

@api.route('/<contract_id>')
@api.param('contract_id', 'contract id')
@api.response(404, 'Contract Not Found')
class Contract(Resource):
    @api.doc('Get Contract Information')
    def get(self, contract_id):
        response = ep_contract.get_contract_information(contract_id)
        return {
            'result':response
        }