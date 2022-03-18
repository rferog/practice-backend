import graphene
from graphene_django.filter import (
    DjangoFilterConnectionField,
)
from graphene_django.types import (
    DjangoObjectType,
    ObjectType,
)
from rferog.models import (
    Comment,
    Post,
    Topic,
)


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class PostType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        posts = DjangoFilterConnectionField(PostType)


class Query(ObjectType):
    comment = graphene.Field(CommentType, id=graphene.String())
    post = graphene.Field(PostType, id=graphene.String())
    posts = graphene.List(PostType)
    topic = graphene.Field(TopicType, id=graphene.String())
    topics = graphene.List(
        TopicType,
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    def resolve_comment(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Comment.objects.get(pk=id)

        return None

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Post.objects.get(pk=id)

        return None

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()
    
    def resolve_topic(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Topic.objects.get(pk=id)

        return None

    def resolve_topics(self, info, first=None, skip=None, **kwargs):
        qs = Topic.objects.all()

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs


class CreateComment(graphene.Mutation):
    class Arguments:
        parent_comment_id = graphene.ID()
        content = graphene.String(required=True)
        author = graphene.String(required=True)
        parent_post = graphene.String(required=True)

    success = graphene.Boolean()
    comment = graphene.Field(CommentType)

    @staticmethod
    def mutate(root, info, content, author, parent_post, parent_comment_id = None,):
        success = True
        existing_post_instance = Post.objects.get(pk=parent_post)
        comment_instance = Comment(
            parent_comment_id=parent_comment_id,
            content=content,
            author=author,
            parent_post=existing_post_instance
            )
        comment_instance.save()
        return CreateComment(success=success, comment=comment_instance)


class UpdateComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        parent_id = graphene.ID(required=True)
        content = graphene.String()
        author = graphene.String()
        parent_post = graphene.String()

    success = graphene.Boolean()
    comment = graphene.Field(CommentType)

    @staticmethod
    def mutate(root, info, id, input=None):
        success = False
        comment_instance = Comment.objects.get(pk=id)
        if comment_instance:
            success = True
            comment_instance.content = input.content
            comment_instance.save()
            return UpdateComment(success=success, comment=comment_instance)
        return UpdateComment(success=success, comment=None)


class CreatePost(graphene.Mutation):
    ## TODO: The author shouldn't be taken as input from the front
    ## to prevent user impersonation
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author = graphene.String(required=True)
        parent_topic = graphene.String()

    success = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, title, content, author, parent_topic):
        success = True
        parent_topic_instance = Topic.objects.get(pk=parent_topic)
        post_instance = Post(
            votes=0,
            title=title,
            author=author,
            content=content,
            parent_topic=parent_topic_instance,
            )
        post_instance.save()
        return CreatePost(success=success, post=post_instance)


class UpdatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        votes = graphene.Int()

    success = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, id, title, content, votes):
        success = False
        post_instance = Post.objects.get(pk=id)
        if post_instance:
            success = True
            post_instance.votes = votes
            post_instance.title = title
            post_instance.content = content
            post_instance.save()
            return UpdatePost(success=success, post=post_instance)
        return UpdatePost(success=success, post=None)


class CreateTopic(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    success = graphene.Boolean()
    topic = graphene.Field(TopicType)

    @staticmethod
    def mutate(root, info, name, description):
        success = True
        topic_instance = Topic(
            name=name,
            description=description,
            )
        topic_instance.save()
        return CreateTopic(success=success, topic=topic_instance)


class UpdateTopic(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    success = graphene.Boolean()
    topic = graphene.Field(TopicType)

    @staticmethod
    def mutate(root, info, id, name, description):
        success = False
        topic_instance = Topic.objects.get(pk=id)
        if topic_instance:
            success = True
            topic_instance.name = name
            topic_instance.description = description
            topic_instance.save()
            return UpdateTopic(success=success, post=topic_instance)
        return UpdateTopic(success=success, topic=None)


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    create_post = CreatePost.Field()
    create_topic = CreateTopic.Field()
    update_comment = UpdateComment.Field()
    update_post = UpdatePost.Field()
    update_topic = UpdateTopic.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
