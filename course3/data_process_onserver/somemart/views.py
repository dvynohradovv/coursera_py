import json

import marshmallow.exceptions
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.forms import ModelForm, CharField
from django.views.decorators.csrf import csrf_exempt

from marshmallow import Schema, fields, validate

from .models import Item, Review


class AddItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "price"]

    def clean_title(self):
        data = self.cleaned_data["title"]
        if data == "" or len(data) > 64:
            print(type(data))
            raise ValidationError("Title validation error")
        return data

    def clean_description(self):
        data = self.cleaned_data["description"]
        if data == "" or len(data) > 1024:
            print(type(data))
            raise ValidationError("Description validation error")
        return data

    def clean_price(self):
        data = self.cleaned_data["price"]
        if not isinstance(data, int) or (data < 1 or data > 1000000):
            print(type(data))
            raise ValidationError("Price validation error")
        return data


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        # Здесь должен быть ваш код
        try:
            json_request = json.loads(request.body)

            itemform = AddItemForm(json_request)

            if itemform.is_valid():
                item = Item(title=itemform.cleaned_data["title"],
                            description=itemform.cleaned_data["description"],
                            price=itemform.cleaned_data["price"])
                item.save()
                data = {"id": item.id}
                return JsonResponse(data, status=201)
            return JsonResponse({"error": "Validation error"}, status=400)
        except Exception as ex:
            return JsonResponse({"error": str(ex)}, status=400)


class PostReviewSchema(Schema):
    text = fields.Str(required=True, validate=validate.Length(max=1024))
    grade = fields.Int(required=True, validate=validate.Range(min=1, max=10))


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        # Здесь должен быть ваш код
        try:
            json_request = json.loads(request.body)
            schema = PostReviewSchema(strict=True)
            data = schema.load(json_request)
            item = get_object_or_404(Item, id=int(item_id))
            review = Review(grade=data.data["grade"], text=data.data["text"], item=item)
            review.save()
            return JsonResponse({"id": review.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except marshmallow.exceptions.ValidationError as exc:
            return JsonResponse({'errors': exc.messages}, status=400)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        # Здесь должен быть ваш код
        data = {
            'id': '',
            'title': '',
            'description': '',
            'price': '',
            'reviews': []
        }
        item = get_object_or_404(Item, id=int(item_id))
        data["id"] = item.id
        data["title"] = item.title
        data["description"] = item.description
        data["price"] = item.price

        reviews = Review.objects.filter(item=item)
        if reviews.count() > 5:
            reviews = reviews.order_by("-id")[:5]
            
        for r in reviews:
            data["reviews"].append({
                "id": r.id,
                "text": r.text,
                "grade": r.grade
            })
        return JsonResponse(data, status=200)
