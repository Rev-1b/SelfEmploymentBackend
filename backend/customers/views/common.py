from rest_framework import exceptions


def get_customer_id(self):
    customer_id = self.request.query_params.get('customer_id', None)
    if customer_id is None:
        raise exceptions.ValidationError(f'No "customer_id" specified in request parameters')
    return customer_id


__all__ = ['get_customer_id']
