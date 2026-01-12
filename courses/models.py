from django.db import models


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='photos/', verbose_name='превью курса')
    description = models.TextField(verbose_name='описание курса')

    def __str__(self):
        return f"Название курса: {self.name}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    preview = models.ImageField(upload_to='photos/', verbose_name='превью урока')
    video_url = models.CharField(max_length=200, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return f"Название урока: {self.name}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
