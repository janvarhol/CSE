# from unittest import TestCase
import unittest
from unittest import TestCase

import demo


class demoTest(unittest.TestCase):
    # def setUp(self) -> None:  #python3 syntax only
    def setUp(self):
        name = 'Adrian'
        self.contact = demo.add_contact(name)

    # def tearDown(self) -> None:  #python3 syntax only
    def tearDown(self):
        pass

    def test_add_contact(self):
        '''
        Test proper addition of a new contact
        '''
        # self.fail()
        self.assertEqual({'person': {'Adrian': {}}}, self.contact)

    def test_get_missing_contact(self):
        '''
        Test if KeyError is raised when get_contact() is called for a missing person
        '''
        with self.assertRaises(KeyError):
            demo.get_contact('FakePerson')

    def test_maintenance_check(self):
        '''
        Test if KeyError is raised when get_contact() is called for a missing person
        '''
        self.assertTrue(demo.maintenance_check())

    def test_get_persons(self):
        '''
        Test if person in persons
        '''
        self.assertIn('Adrian', demo.get_persons())

    '''
    # Work in progress, function not ready
    # Skip this test meanwhile
    @unittest.skip("Work in Progress")
    def test_TBD(self):
        self.assertFalse(demo.TBD())
    '''

