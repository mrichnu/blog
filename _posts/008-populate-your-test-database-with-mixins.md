Title: Populate Your Test Database With Mixins
Date: 2014-01-24 12:30
Tags: python, django, testing
Slug: populate-your-test-database-with-mixins
Author: Matthew Rich
Summary: Maintaining fixtures got you down? Use a mixin!

While Django has support for [loading
fixtures](https://docs.djangoproject.com/en/1.6/topics/testing/tools/#fixture-loading)
in its unit testing tools, I have found that maintaining fixtures over time is
nothing less than a giant pain in the butt. As your model definitions change
over time, remembering to re-run `manage.py dumpdata myapp >fixtures.json` any
time your fixtures are affected is something I guarantee you will forget to do.
Not to mention the fact that your database may or may not contain records
suitable for testing at any given time. Then all of your unit tests have blown
up, it takes you a little bit of time to figure out why, and before you know it
you are cursing and out of your flow.

For a time I tried using Alex Gaynor's
[django-fixture-generator](https://github.com/alex/django-fixture-generator)
but that only solved the problem of creating the records you want to test, not
the problem of fixtures sitting on disk that are out of sync with your model
schema.

After being introduced to Django class-based views' mixin-heavy style, I cooked
up a technique for unit test `TestCase` classes to create the records they need
at runtime, thus bypassing the need for fixtures. In an apps
`tests/__init__.py` I create a `PopulateDbMixin`:

    class PopulateDbMixin(object):
        def populate_db(self):
            """Assume our app has Recipe and Ingredient models"""
            self.models = {}

            self.models['recipes'] = {}
            self.models['recipes']['bread'] = \
                Recipe.objects.create(name='bread')

            self.models['ingredients'] = {}
            self.models['ingredients']['flour'] = \
                Ingredient.objects.create(name='flour')
            self.models['ingredients']['yeast'] = \
                Ingredient.objects.create(name='yeast')

        
We can now include this mixin in our `TestCase` classes and run its
`populate_db` method in `setUp` and have freshly baked bread in each of our
test methods:

    class DeliciousTestCase(PopulateDbMixin, TestCase):
        def setUp(self):
            self.populate_db()

        def test_can_bake_bread(self):
            bread_recipe = self.models['recipes']['bread']
            yeast = self.models['ingredients']['yeast']

            bread_recipe.ingredients.add(yeast)

            self.assert_(not bread_recipe.goes_horribly_wrong())

The Django `TestCase` will take care of clearing out the database in between
each run; we're just running `populate_db` instead of the usual fixture-loading
pattern.

This particular technique may be old as time and in use by many teams, but I
haven't seen it written down anywhere so I thought I would share.
