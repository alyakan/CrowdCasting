from haystack import indexes
from main.models import Actor


class ActorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr="user__username")
    experience = indexes.CharField()
