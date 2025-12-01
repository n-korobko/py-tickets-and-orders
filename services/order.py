from typing import List, Dict, Optional
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from django.contrib.auth import get_user_model
from db.models import Order, Ticket
from django.db.models import QuerySet


@transaction.atomic
def create_order(
    tickets: List[Dict[str, int]],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user_model = get_user_model()
    user = user_model.objects.get(username=username)

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        created_at = timezone.now().replace(microsecond=0)

    order = Order.objects.create(
        user=user,
        created_at=created_at,
    )

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order,
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
