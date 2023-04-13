from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    abort
)

from service.entities import DeliveryData, DeliveryResult
from service.main import DeliveryService

from marshmallow import ValidationError
from schema import(
    CalcSchema,
    CalcPostcode,
    BadRequestSchema,
    ServiceExceptionSchema
)

from service.exceptions import ServiceException

def create_app():
    app = Flask(__name__)

    @app.errorhandler(400)
    def bad_request_handler(ex: ValidationError):
        return BadRequestSchema().dump(ex), 400

    @app.errorhandler(500)
    def bad_request_handler(ex: ServiceException):
        return ServiceExceptionSchema().dump(ex), 500

    @app.route("/")
    def hello_world():
        return render_template("index.html")
            
    @app.route("/calc/", methods=["post"])
    def calc() -> DeliveryResult:

        schema = CalcSchema()
        service = DeliveryService()
        try:
            request_data: DeliveryData = request.json
            data = service.calc(data = schema.load(request_data))
        except ValidationError as ex:
            abort(400, ex)
        except ServiceException as ex:
            abort(500, ex)
        else:
            return schema.dump(data)

    @app.route("/postcode/", methods=["post"])
    def postcode():

        schema = CalcPostcode()
        service = DeliveryService()
        try:
            request_data: DeliveryData = request.json
            data = service.calc(data = schema.load(request_data))
        except ValidationError as ex:
            abort(400, ex)
        except ServiceException as ex:
            abort(500, ex)
        else:
            return postcode.dump(data)
    return app

app = create_app()