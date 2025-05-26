#!/usr/bin/env python3


from my_blog.database import Base, engine, session_maker
from my_blog.models.post import Post
from my_blog.models.tag import Tag
from my_blog.models.user import User


def create_table():
    Base.metadata.create_all(engine)

def main():
    create_table()
    with session_maker() as session:
        new_user = User(username="Mutant", email="mutant@gmail.com")
        session.add(new_user)

        new_tag_1 = Tag(name="Тренировка в спортзале")
        session.add(new_tag_1)

        new_tag_2 = Tag(name="Тренировка на улице")
        session.add(new_tag_2)

        new_post_1 = Post(
            user_id=1,
            tag_id=1,
            title="Fran",
            description=(
                "Задача: выполнить с максимальной интенсивностью (мощностью)\n"
                "Выполнить: 3 раунда из 21-15-9 повторений\n"
                "Задание:\n"
                "Выбросы штанги, 45 кг\n"
                "Подтягивание на турнике"
            )
        )
        session.add(new_post_1)

        new_post_2 = Post(
            user_id=1,
            tag_id=2,
            title="Hannibal king",
            description=(
                "Задача: Закончить задание за минимальное время\n"
                "Задание:\n"
                "Делается последовательно с минимальным отдыхом:\n"
                "Отжимания от пола – 30/29/28/27/26/25/24/23/22/21/20\n"
                "Подтягивания (прямой хват) – 10/9/8/7/6/5/5/5/5/5/5\n"
                "Отжимания на брусьях – 20/19/18/17/16/15/14/13/12/11/10\n"
                "Подтягивания(обратный хват) – 10/9/8/7/6/5/5/5/5/5/5"
            )
        )
        session.add(new_post_2)

        session.commit()

        posts = session.query(Post).filter(Post.user_id == 1).all()

        for post in posts:
            result = (
                f"{post.users.username}\n"
                f"{post.title}\n"
                f"{post.description}\n"
                f"{post.tags.name}"
            )
            print(result)


if __name__ == '__main__':
    main()
