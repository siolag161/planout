
    

#===============================================================================
class BehaviorTestCaseMixin(object):
    def get_model(self):
            return getattr(self, 'model')

    def create_instance(self, **kwargs):
        raise NotImplementedError("Implement me")

class AuthenticatedMixin(BehaviorTestCaseMixin):    
    def create_user(self, **kwargs):
	from django.contrib.auth import get_user_model 
	User = get_user_model()
	username = 'testuser'
	password = 'testpass'
	email = 'bunbun@gmail.com'
	self.user = User.objects.create_user( email=email, password=password)
	logged_in = self.client.login(username = username, email = email, password = password)
	#Image.init()    
	self.assertTrue(logged_in)
	#raise NotImplementedError("Implement me")
	return self.user
#===============================================================================

#===============================================================================
class PostedModelTests(BehaviorTestCaseMixin):
    def create_new_user(self, **kwargs):
        raise NotImplementedError("Implement me")
	
    def test_posted(self):
	self.poster = self.create_new_user()
	obj = self.create_instance(poster = self.poster)
	self.assertEqual(obj.poster, obj.poster)
	


#===============================================================================
class TimeStampedModelTests(BehaviorTestCaseMixin):   

    def test_auto_created(self):
	from django.utils.timezone import now	
	obj = self.create_instance()
	right_now = now()
	delta = (obj.created - right_now).total_seconds()
	self.assertTrue(abs(delta) < 2.0)

    def test_auto_modified(self):
	from django.utils.timezone import now	
	obj = self.create_instance()
	right_now = now()
	delta = (obj.modified - right_now).total_seconds()
	self.assertTrue(abs(delta) < 2.0)

#===============================================================================
class SluggedModelTests(BehaviorTestCaseMixin):
    
    def test_slug(self):
	
	name = "random name like this"
	slug_name = "random-name-like-this"
	
	obj = self.create_instance(name=name)
	self.assertEqual(obj.name, name)
	
	import slugify	
	self.assertEqual(slugify.slugify(obj.name),  slug_name)
	
	self.assertTrue(hasattr(obj, "url_name"))

	self.assertEqual(obj.slug, "random-name-like-this")

	# self.assertEqual(obj.get_absolute_url(), "%s/%s" %(obj.pk, obj.slug))

	# if hasattr(obj, "uuid"):
	#     obj.url_kwargs = {'uuid': obj.uuid, 'slug': obj.slug}
	# self.assertEqual(obj.get_absolute_url(), "%s/%s" %(obj.uuid, obj.slug))

# #===============================================================================	
# class TimeStampedModel(models.Model):
#     created = AutoCreatedField(_('created'))
#     modified = AutoLastModifiedField(_('modified'))

#     class Meta:
#         abstract = True
# #===============================================================================
# class TimeFramedModel(models.Model):
#     start_time = models.DateTimeField(_('start'), null=True, blank=True)
#     end_end = models.DateTimeField(_('end'), null=True, blank=True)

#     class Meta:
#         abstract = True

