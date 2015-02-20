
import logging
logger = logging.getLogger('werkzeug')

class FormTests(object):
    
    def get_form_data(self):
	raise NotImplementedError("please implement this")

    def test_form_valid(self):
	form_data = self.get_form_data()
	form = self.form_class(data=form_data)
	rs = form.is_valid()
	logger.critical(form.errors)
	self.assertEqual(rs, True)
