from datetime import date, timedelta

from duffel_api import Duffel

if __name__ == "__main__":
    print("Duffel Flights API - book and change example")
    client = Duffel()
    departure_date = date.today().replace(date.today().year + 1)
    offer_request_slices = [
        {
            "origin": "LHR",
            "destination": "STN",
            "departure_date": departure_date.strftime("%Y-%m-%d"),
        },
    ]
    offer_request = (
        client.offer_requests.create()
        .passengers([{"type": "adult"}])
        .slices(offer_request_slices)
        .execute()
    )

    print("Created offer request: %s" % (offer_request.id))

    offers = client.offers.list(offer_request.id)
    offers_list = list(enumerate(offers))

    print("Got %d offers" % len(offers_list))

    selected_offer = offers_list[0][1]

    print("Selected offer %s to book" % (selected_offer.id))

    priced_offer = client.offers.get(selected_offer.id)

    print(
        "The final price for offer %s is %s (%s)"
        % (priced_offer.id, priced_offer.total_amount, priced_offer.total_currency)
    )

    payments = [
        {
            "currency": selected_offer.total_currency,
            "amount": selected_offer.total_amount,
            "type": "balance",
        }
    ]
    passengers = [
        {
            "born_on": "1976-01-21",
            "email": "conelia.corde@duffel.com",
            "family_name": "Corde",
            "gender": "f",
            "given_name": "Conelia",
            "id": offer_request.passengers[0].id,
            "phone_number": "+442080160508",
            "title": "ms",
        }
    ]

    order = (
        client.orders.create()
        .payments(payments)
        .passengers(passengers)
        .selected_offers([selected_offer.id])
        .execute()
    )

    print(
        "Created order %s with booking reference %s"
        % (order.id, order.booking_reference)
    )

    order_change_request_slices = {
        "add": [
            {
                "cabin_class": "economy",
                "departure_date": (departure_date + timedelta(weeks=4)).strftime(
                    "%Y-%m-%d"
                ),
                "origin": "LHR",
                "destination": "STN",
            }
        ],
        "remove": [
            {
                "slice_id": order.slices[0].id,
            }
        ],
    }

    order_change_request = (
        client.order_change_requests.create(order.id)
        .slices(order_change_request_slices)
        .execute()
    )

    order_change_offers = client.order_change_offers.list(order_change_request.id)
    order_change_offers_list = list(enumerate(order_change_offers))

    print(
        "Got %d options for changing the order; picking first option"
        % (len(order_change_offers_list))
    )

    order_change = client.order_changes.create(order_change_offers_list[0][1].id)

    print("Created order change %s, confirming..." % order_change.id)

    payment = {
        "amount": order_change.change_total_amount,
        "currency": order_change.change_total_currency,
        "type": "balance",
    }

    client.order_changes.confirm(order_change.id, payment)

    print(
        "Processed change to order %s costing %s (%s)"
        % (
            order.id,
            order_change.change_total_amount,
            order_change.change_total_currency,
        )
    )
