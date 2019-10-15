from flask_restplus import Namespace, Resource, fields


api = Namespace('ep_supplier', description="EP Supplier records")

@api.route('/')
class SupplierList(Resource):
    @api.doc('list_supplier')
    def get(self):
        return {
            'supplier':"list of supplier"
        }