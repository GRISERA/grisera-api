from grisera.services.not_implemented_service_factory import NotImplementedServiceFactory


class Service:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Service, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.service_factory = NotImplementedServiceFactory()

    def get_service_factory(self):
        return self.service_factory


service = Service()
