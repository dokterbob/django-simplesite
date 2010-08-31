from django.test import TestCase 

from simplesite.models import *


class TemplateTestMixin(object):
    def assertContextContains(self, response, variable_name, variable_value=None):
        context = response.context
        
        try:
            value = context[variable_name]
        except KeyError:
            self.fail('Context does not contain %s; it contains: %s' \
                        % (variable_name, context))
                    
        if variable_value:
            self.assertEquals(value, variable_value)

class SimpleSiteTestCase(TestCase, TemplateTestMixin):       
    urls = 'simplesite.tests.testapp.urls'
    
    def setUp(self):
        """ We'll setup the following structure:
            m1 -- sm1
            m2 -- p1 
            m3 -- sm2
                ` sm3 -- p2
        """
        self.p1 = Page(title='bla 1', content='Blabla')
        self.p1.save()

        self.p2 = Page(title='bla 2', content='Blabla')
        self.p2.save()

        self.m1 = Menu(slug='test-1', title='Test item 1')
        self.m1.save()
        
        self.m2 = Menu(slug='test-2', title='Test item 2', page=self.p1)
        self.m2.save()

        self.m3 = Menu(slug='myview', title='Test item 3')
        self.m3.save()

        self.sm1 = Submenu(slug='s-1', title='Submenu item 1', menu=self.m1)
        self.sm1.save()

        self.sm2 = Submenu(slug='s-1', title='Submenu item 1', menu=self.m3)
        self.sm2.save()

        self.sm3 = Submenu(slug='s-2', title='Submenu item 1', menu=self.m3, page=self.p2)
        self.sm3.save()

class RequestContextMenuTests(SimpleSiteTestCase):
    
    def test_normalview(self):
        # As myview actually exists in the site, it should give no error
        response = self.client.get('/myview/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertContextContains(response, 'menu_current', self.m3)
        self.assertContextContains(response, 'menu_list')
    
    def test_nomenunopage(self):
        response = self.client.get('/blabla/')
        self.failUnlessEqual(response.status_code, 404)
        
    def test_menunopage(self):
        response = self.client.get('/test-1/')
        self.failUnlessEqual(response.status_code, 404)

    def test_menupage(self):
        response = self.client.get('/test-2/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertContextContains(response, 'menu_current', self.m2)
        self.assertContextContains(response, 'menu_list')
