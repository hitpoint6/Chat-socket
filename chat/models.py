from django.contrib.auth import get_user_model

from django.db import models


User = get_user_model()

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username}"


class Room(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    staff_only = models.BooleanField(default=False)
    participants = models.ManyToManyField(Participant, blank=True)

    def count_message_per_room(self):
        return len(self.message_set.all())

    def count_new_messages(self, user):
        counter = 0
        for m in self.message_set.all():
            if user.participant not in m.readers.all():
                counter +=1
        return counter

class Message(models.Model):
    author = models.ForeignKey(Participant, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    readers = models.ManyToManyField(Participant, related_name="read_messages", blank=True)

    def __str__(self):
        return f"{self.author} said {self.content} in Room {self.room.id}"