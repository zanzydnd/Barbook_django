from .user import BarbookUser
from .stuff import Cocktail
from django.db import models


class CommentOnCocktail(models.Model):
    text = models.TextField(max_length=250)
    author = models.ForeignKey(BarbookUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)

    class Meta:
        db_table = "comment_on_cocktail"


class AnswerOnComment(models.Model):
    main_comment = models.ForeignKey(CommentOnCocktail, on_delete=models.CASCADE)
    answer_author = models.ForeignKey(BarbookUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    answer_on_answer = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "answer_on_comment"
