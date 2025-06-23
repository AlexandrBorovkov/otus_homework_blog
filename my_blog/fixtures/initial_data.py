from sqlalchemy import select

from my_blog.database import async_session_maker
from my_blog.posts.models import Post
from my_blog.tags.models import Tag
from my_blog.users.models import User


async def create_initial_data():
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        if result.scalars().first() is not None:
            return
        user = User(
            username="testuser",
            email="testuser@example.com",
            hashed_password="$2b$12$JeplP9OPt1QAoNZYL1dVy.1ly7Ak2se9PSpXXZjXAxKcwMba4waTG"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        tags = [
            Tag(name="Тренировка в спортзале", user_id=user.id),
            Tag(name="Тренировка на улице", user_id=user.id),
        ]
        session.add_all(tags)
        await session.commit()

        tag_ids = [tag.id for tag in tags]
        posts = [
            Post(
                title="Fran",
                description=(
                    "Задача: выполнить с максимальной интенсивностью<br>"
                    "Выполнить: 3 раунда из 21-15-9 повторений<br>"
                    "Задание:<br>"
                    "Выбросы штанги, 45 кг<br>"
                    "Подтягивание на турнике"
                ),
                user_id=user.id,
                tag_id=tag_ids[0]
            ),
            Post(
                title="Hannibal king",
                description=(
                    "Задача: Закончить задание за минимальное время<br>"
                    "Задание:<br>"
                    "Делается последовательно с минимальным отдыхом:<br>"
                    "Отжимания от пола – 30/29/28/27/26/25/24/23/22/21/20<br>"
                    "Подтягивания (прямой хват) – 10/9/8/7/6/5/5/5/5/5/5<br>"
                    "Отжимания на брусьях –20/19/18/17/16/15/14/13/12/11/10<br>"
                    "Подтягивания(обратный хват) – 10/9/8/7/6/5/5/5/5/5/5"
                ),
                user_id=user.id,
                tag_id=tag_ids[1]
            ),
            Post(
                title="Синди",
                description=(
                    "Задача: Максимальное количество раундов за 20 минут<br>"
                    "Задание:<br>"
                    "5 подтягиваний на турнике<br>"
                    "10 отжиманий от пола<br>"
                    "15 воздушных приседаний"
                ),
                user_id=user.id,
                tag_id=tag_ids[1]
            )
        ]
        session.add_all(posts)
        await session.commit()
