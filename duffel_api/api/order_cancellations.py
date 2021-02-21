from ..http_client import HttpClient
from ..models import OrderCancellation


class OrderCancellationClient(HttpClient):
    """To cancel an order, you'll need to create an order cancellation, check the
    refund_amount returned, and, if you're happy to go ahead and cancel the order.

    The refund specified by refund_amount, if any, will be returned to your original
    payment method (i.e. your Duffel balance). You'll then need to refund your customer
    (e.g. back to their credit/debit card).
    """

    def __init__(self, **kwargs):
        self._url = '/air/order_cancellations'
        super().__init__(**kwargs)

    def create(self, order_id):
        """To begin the process of cancelling an order you need to create an order
        cancellation. The OrderCancellation will contain the refund_amount due from the
        Airline.

        To proceed, you must confirm the cancellation using the Confirm an order
        cancellation endpoint.

        """

        res = self.do_post(self._url, body={'data': {'order_id': order_id}})
        return OrderCancellation(res['data'])

    def confirm(self, id_):
        """Once you've created a pending order cancellation, you'll know the refund_amount you're
        due to get back.

        To actually cancel the order, you'll need to confirm the cancellation. The booking
        with the airline will be cancelled, and the refund_amount will be returned to the
        original payment method (i.e. your Duffel balance). You'll then need to refund
        your customer (e.g. back to their credit/debit card).

        """

        url = '{}/{}/actions/confirm'.format(self._url, id_)
        return OrderCancellation(self.do_post(url)['data'])