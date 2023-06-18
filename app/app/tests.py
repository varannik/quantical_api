
from django.test import SimpleTestCase

from app import calc 


class Calctest ( SimpleTestCase):
    
    def test_power(self):
        res = calc.power(2,2)
        self.assertEqual(res , 4)


    def test_add(self):
        res = calc.add(2,2)
        self.assertEqual(res,4)