import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False for questions whose pub is in the future"""
        time = timezone.now() +  datetime.timedelta(days=30)
        future_question = Question(question_text="¿What is the fastest car in the world?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

def create_question (question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """if no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question(self):
        """Question with a pub_date in the future aren't displayed on the index page"""
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """Question with a pub_date in the past are displayed on the index page"""
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

