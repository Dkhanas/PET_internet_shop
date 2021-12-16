from django import forms

ORDER_TYPES = (
    ("created_at", "from new to old"),
    ("-created_at", "from old to new"),
    ("price", "by price in ascending"),
    ("-price", "by price in descending"),
)


class OrderItems(forms.Form):
    order_type = forms.ChoiceField(choices=ORDER_TYPES)
