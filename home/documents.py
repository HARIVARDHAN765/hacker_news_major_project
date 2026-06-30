from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from .models import Post

post_index = Index("posts")


@registry.register_document
class PostDocument(Document):

    title = fields.TextField(
        fields={
            "suggest": fields.SearchAsYouTypeField(),
        },
    )

    user = fields.TextField(
        attr="user.username",
    )

    class Index:
        name = "posts"

    class Django:
        model = Post

        fields = [
            "id",
            "text",
            "url",
            "post_type",
            "created_at",
        ]