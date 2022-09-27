VERSION = 0.1

SWAGGER_TEMPLATE = {
    "uiversion": 3,
    "swagger": "2.0",
    "info": {
        "title": "Rule Engine",
        "description": "Rule Engine API",
        "contact": {
            "responsibleOrganization": "Me",
            "responsibleDeveloper": "Joao Almeida",
        },
        "termsOfService": "http://me.com/terms",
        "version": "0.0.1",
    },
    # "host": "http://bibliovigilancia.gim.med.up.pt/",  # overrides localhost:5000
    "basePath": "api",  # base bash for blueprint registration
    "schemes": ["http", "https"],
}
