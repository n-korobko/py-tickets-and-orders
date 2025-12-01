from typing import List, Dict, Optional
from datetime import datetime

from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession
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
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M").replace(microsecond=0)
    else:
        created_at = timezone.now().replace(microsecond=0)

    order = Order.objects.create(
        user=user,
        created_at=created_at,
    )

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(id=ticket_data["movie_session"]),
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            order=order,
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    queryset = Order.objects.select_related("user")

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
