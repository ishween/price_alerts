from flask import  Blueprint


item_blueprint = Blueprint('items', __name__)
#never called - delete them later

@item_blueprint.route('/item/<string:name>')
def item_page(name):
    pass


@item_blueprint.route('/load')
def load_item():
    """
    loads an item's data using their stores and return JSON representation for it
    :return:
    """
    pass