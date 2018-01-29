# -*- coding: utf-8 -*-
from sc.photogallery.utils import human_readable_size

import unittest


class UtilsTestCase(unittest.TestCase):

    def test_human_readable_size(self):
        with self.assertRaises(ValueError):
            human_readable_size(-5)

        self.assertEqual(human_readable_size(0), '0')
        self.assertEqual(human_readable_size(5), '5')
        self.assertEqual(human_readable_size(5000), '4.9 kB')
        self.assertEqual(human_readable_size(5000000), '4.8 MB')
        self.assertEqual(human_readable_size(5000000000), '4.7 GB')
        self.assertEqual(human_readable_size(5000000000000), '4656.6 GB')
