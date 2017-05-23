from peewee import * 
db = SqliteDatabase('data.db')


class Person(Model):
	class Meta:
		database = db

	name = CharField()
	surname = CharField()


def initialize():	
	Person.create_table(True)