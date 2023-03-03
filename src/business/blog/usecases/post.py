from src.business.blog.dto import UpdatePostDTO
from src.business.blog.dto.post import (
    CreatePostDTO, PostDTO,
)
from src.business.common.usecases.base import BaseUseCase

from src.dal.db.uow import UnitOfWork


class PostUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class GetPostById(PostUseCase):
    async def __call__(self, id_: int) -> PostDTO:
        post = await self.uow.blog_holder.post_repo.get_post_by_id(
            id_
        )
        return post


class CreatePost(PostUseCase):
    async def __call__(self, post_dto: CreatePostDTO) -> PostDTO:
        post = await self.uow.blog_holder.post_repo.create_post(
            post_dto
        )
        await self.uow.commit()
        return post


class GetPosts(PostUseCase):
    async def __call__(self) -> list[PostDTO]:
        posts = await self.uow.blog_holder.post_repo.get_all_posts()
        return posts


class UpdatePost(PostUseCase):
    async def __call__(self, post_update_dto: UpdatePostDTO) -> None:
        await self.uow.blog_holder.post_repo.update_post(
            post_update_dto.id,
            **post_update_dto.dict(
                exclude_none=True,
                exclude=set('id')
            )
        )


class PostServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_post(self, user_dto: CreatePostDTO) -> PostDTO:
        return await CreatePost(self.uow)(user_dto)

    async def get_all_posts(self) -> list[PostDTO]:
        return await GetPosts(self.uow)()

    async def get_post_by_id(self, id_: int) -> PostDTO:
        return await GetPostById(self.uow)(id_)

    async def update_post(
            self,
            update_post_dto: UpdatePostDTO
    ) -> PostDTO:
        await UpdatePost(self.uow)(update_post_dto)
        return await GetPostById(self.uow)(update_post_dto.id)
