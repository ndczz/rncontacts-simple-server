import falcon
import json
from models import Person
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee_validates import ModelValidator, StringField
import peewee

class XValidator(ModelValidator):
	name = StringField(required=True, min_length=5)
	surname = StringField(required=True, min_length=5)


class MultiplePersons(object):
	def on_get(self, req, resp):
		resp.status =  falcon.HTTP_200
		lst = [model_to_dict(i) for i in Person.select()]
		resp.body = json.dumps(lst)

	def on_post(self, req, resp):
		
		data = json.loads(req.stream.read())
		print(data)
		person = Person(**data)				
		
		validator = XValidator(person)
		validator.validate()
		if len(validator.errors) == 0 :
			resp.status = falcon.HTTP_200
			person.save()
			resp.body = json.dumps(model_to_dict(person))
		else:
			resp.status = falcon.HTTP_404
			er = {'errors': validator.errors}
			resp.body = json.dumps(er)
		

class SinglePerson(object):
	def on_get(self, req, resp, id):
		resp.status = falcon.HTTP_200
		p = Person.select().where(Person.id == id).get()
		resp.body = json.dumps(model_to_dict(p))

	def on_put(self, req, resp, id):
		resp.status = falcon.HTTP_200
		person = Person.select().where(Person.id == id).get()
		data = json.loads(req.stream.read())
		person.update(**data)
		resp.body = json.dumps(model_to_dict(person))

	def on_delete(self, req, resp, id):
		resp.status = falcon.HTTP_200
		person = Person.select().where(Person.id == id).get()
		if person:
			person.delete()		
		resp.body = 'ok'

