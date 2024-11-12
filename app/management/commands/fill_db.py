import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The filling ratio for entities')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        # Создание пользователей с уникальными именами
        users = set()
        while len(users) < ratio:
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Создание случайного имени
            user = User.objects.create_user(username=username, password='password')  # Уникальные имена
            users.add(user)

        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))

        tags = []
        for _ in range(ratio):
            tag = Tag.objects.create(name=f'tag_{_}')
            tags.append(tag)

        self.stdout.write(self.style.SUCCESS(f'Created {len(tags)} tags'))

        questions = []
        for _ in range(ratio * 10):
            question = Question.objects.create(
                user=random.choice(list(users)),  # Преобразование в список для выбора
                title=f'Question title {_}',
                text=f'Question text {_}')
            question.tags.add(
                *random.sample(tags, k=random.randint(1, min(3, len(tags)))))
            questions.append(question)

        self.stdout.write(self.style.SUCCESS(f'Created {len(questions)} questions'))

        answers = []
        for _ in range(ratio * 100):
            question = random.choice(questions)
            answer = Answer.objects.create(
                question=question,
                user=random.choice(list(users)),  # Преобразование в список для выбора
                text=f'Answer text {_}'
            )
            answers.append(answer)

        self.stdout.write(self.style.SUCCESS(f'Created {len(answers)} answers'))

        question_likes = []
        for _ in range(ratio * 200):
            user = random.choice(list(users))
            question = random.choice(questions)
            if not QuestionLike.objects.filter(user=user, question=question).exists():
                like = QuestionLike.objects.create(user=user, question=question)
                question_likes.append(like)

        self.stdout.write(self.style.SUCCESS(f'Created {len(question_likes)} question likes'))

        answer_likes = []
        for _ in range(ratio * 200):
            user = random.choice(list(users))
            answer = random.choice(answers)
            if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                like = AnswerLike.objects.create(user=user, answer=answer)
                answer_likes.append(like)

        self.stdout.write(self.style.SUCCESS(f'Created {len(answer_likes)} answer likes'))
